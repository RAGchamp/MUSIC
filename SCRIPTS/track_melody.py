"""
track_melody.py: follow ONE continuous lead line (e.g. a flute) through a recording.

    python track_melody.py ../REFERENCE-AUDIO-FILES/SONG-3-pehla-nasha-start.wav --lo C4 --hi C7
    python track_melody.py ../REFERENCE-AUDIO-FILES/SONG-3-pehla-nasha-start.wav --check pehla --trust 17.1-44.2
    python track_melody.py ../REFERENCE-AUDIO-FILES/SONG-3-pehla-nasha-start.wav --start 0 --end 17 --out draft.txt

analyze_notes.py keeps the STRONGEST note at each onset, so where a band plays louder than
the tune its notes follow the band. This script instead:

1. scores every note from --lo to --hi in every frame (12 ms) by harmonic salience with few
   harmonics (a flute has a strong fundamental and weak overtones), and lowers a note's score
   when a strong note an octave or a twelfth BELOW it explains it as an overtone (the band);
2. finds the smoothest path through those scores (Viterbi): staying on a note is free, a jump
   costs more the bigger it is, and a 'rest' state takes over where nothing is loud enough;
3. cuts the path into notes: a new note where the pitch changes, or where an onset shows the
   same note being played again; notes shorter than --min-note are merged into a neighbour.

--check <song> compares the draft with that song's lines in song-library.js (how many lines
have the same note at the same moment). --trust a-b reports that score for a stretch you know
is right, which is the way to tune the settings.
"""
import argparse
import re
import sys
from pathlib import Path

import numpy as np

from musicdsp import (load_wav, spectrogram, estimate_tuning, salience, onset_envelope,
                      detect_onsets, midi_to_name, name_to_midi)

HERE = Path(__file__).resolve().parent
LIB = HERE.parent / 'REFERENCE-AUDIO-FILES' / 'song-library.js'


def lead_scores(x, sr, lo, hi, cents, hop=256, n_harm=4, decay=0.6, octave_pen=0.2, twelfth_pen=0.0):
    """Per-frame lead-line score for notes lo..hi (rows) and frame times."""
    base = lo - 24                                   # also measure two octaves below, to spot overtones
    freqs, t, mag = spectrogram(x, sr, win=4096, hop=hop, nfft=8192, fmax=6000)
    S = salience(mag, freqs, base, hi, cents, n_harm=n_harm, decay=decay)
    lead = S[lo - base:].copy()
    for i, m in enumerate(range(lo, hi + 1)):
        lead[i] -= octave_pen * S[m - 12 - base]     # overtone 2 of a note an octave down
        lead[i] -= twelfth_pen * S[m - 19 - base]    # overtone 3 of a note a twelfth down
    lead = np.maximum(lead, 0)
    loud = np.sqrt((mag ** 2).sum(axis=0))
    return lead, t, loud


def viterbi(lead, loud, jump=0.35, per_semi=0.03, rest_level=0.12, rest_cost=0.25):
    """Best path through notes (+ a rest state). Returns state per frame (-1 = rest)."""
    n, T = lead.shape
    norm = lead / (lead.max(axis=0, keepdims=True) + 1e-9)          # 1.0 = this frame's best note
    quiet = loud < rest_level * np.median(loud)
    emis = np.log(norm + 0.05)                                       # n x T
    rest_e = np.where(quiet, 0.0, np.log(0.05) + 0.0)                # rest wins only when it's quiet
    E = np.vstack([emis, rest_e[None, :]])                           # (n+1) x T
    idx = np.arange(n)
    trans = -(jump + per_semi * np.abs(idx[:, None] - idx[None, :]))
    np.fill_diagonal(trans, 0.0)
    full = np.full((n + 1, n + 1), -rest_cost)
    full[:n, :n] = trans
    full[n, n] = 0.0
    score = E[:, 0].copy()
    back = np.zeros((n + 1, T), dtype=np.int16)
    for k in range(1, T):
        cand = score[:, None] + full                                 # from (rows) -> to (cols)
        back[:, k] = cand.argmax(axis=0)
        score = cand.max(axis=0) + E[:, k]
    path = np.empty(T, dtype=np.int32)
    path[-1] = int(score.argmax())
    for k in range(T - 1, 0, -1):
        path[k - 1] = back[path[k], k]
    path[path == n] = -1
    return path


def to_notes(path, t, lo, onsets, min_note=0.07, restrike_gap=0.12):
    """Runs of the same state -> notes [(start, end, midi)], split at onsets inside long runs."""
    notes = []
    k = 0
    T = len(path)
    while k < T:
        j = k
        while j + 1 < T and path[j + 1] == path[k]:
            j += 1
        if path[k] >= 0:
            notes.append([t[k], t[j], lo + int(path[k])])
        k = j + 1
    # merge blips into the longer neighbour
    out = []
    for nt in notes:
        if out and nt[1] - nt[0] < min_note:
            out[-1][1] = nt[1]
            continue
        if out and out[-1][1] - out[-1][0] < min_note and nt[0] - out[-1][1] < 0.05:
            nt[0] = out[-1][0]
            out[-1] = nt
            continue
        out.append(nt)
    # join neighbours that ended up on the same note, then re-split them at real onsets
    joined = []
    for nt in out:
        if joined and joined[-1][2] == nt[2] and nt[0] - joined[-1][1] < 0.05:
            joined[-1][1] = nt[1]
        else:
            joined.append(nt)
    final = []
    for s, e, m in joined:
        cuts = [o for o in onsets if s + restrike_gap < o < e - restrike_gap]
        pts = [s] + cuts + [e]
        for a, b in zip(pts[:-1], pts[1:]):
            final.append((a, b, m))
    return final


def snap_starts(notes, onsets, win=0.09):
    """Move each note start to the nearest onset within win seconds (the path lags a little)."""
    out = []
    for s, e, m in notes:
        near = [o for o in onsets if abs(o - s) <= win]
        if near:
            s = min(near, key=lambda o: abs(o - s))
        out.append((s, e, m))
    return out


def library_lines(song):
    """[(time, [midis])] of the first song in song-library.js whose title or file contains `song`."""
    txt = LIB.read_text(encoding='utf-8')
    for block in re.split(r'\n\s*\{\s*\n', txt):
        if song.lower() in block.lower() and 'notes:' in block:
            lines = re.findall(r"'\s*([\d.]+)\s+(\S+)\s+([\d.]+)[^']*'", block)
            res = []
            for tt, nn, _ in lines:
                body = nn.lstrip('~^')
                res.append((float(tt), [name_to_midi(p.split('@')[0]) for p in body.split('+')]))
            return res
    raise SystemExit('song "%s" not found in song-library.js' % song)


def check(notes, lines, t0=None, t1=None, tol=0.10):
    """How many library lines (in t0..t1) have the draft playing one of their notes at line time + 0.06 s."""
    hit = tot = 0
    bad = []
    for tt, ms in lines:
        if (t0 is not None and tt < t0) or (t1 is not None and tt > t1):
            continue
        tot += 1
        probe = tt + 0.06
        cur = [m for s, e, m in notes if s - tol <= probe <= e + 0.02]
        if any(m in ms for m in cur):
            hit += 1
        else:
            bad.append((tt, ms, cur))
    return hit, tot, bad


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description='Follow one lead line (flute) through a recording.')
    p.add_argument('wav')
    p.add_argument('--lo', default='C4')
    p.add_argument('--hi', default='C7')
    p.add_argument('--start', type=float)
    p.add_argument('--end', type=float)
    p.add_argument('--tuning', type=float)
    p.add_argument('--jump', type=float, default=0.2, help='cost of changing note (higher = fewer, longer notes)')
    p.add_argument('--octave-pen', type=float, default=0.2, help='how much a strong note an octave below counts against a note')
    p.add_argument('--min-note', type=float, default=0.07)
    p.add_argument('--tempo', type=float, default=78, help='only used for the beats column')
    p.add_argument('--check', help='compare with this song in song-library.js (title or file name part)')
    p.add_argument('--trust', help='a-b: seconds where the library is known to be right (reported separately)')
    p.add_argument('--out', help='write the draft lines to this file')
    a = p.parse_args(argv)

    lo, hi = name_to_midi(a.lo), name_to_midi(a.hi)
    x, sr, offset = load_wav(a.wav)                  # whole file: tuning and context
    freqs, _, mag = spectrogram(x, sr, win=4096, hop=512, nfft=8192, fmax=6000)
    cents = a.tuning if a.tuning is not None else estimate_tuning(mag, freqs)
    print('[track] %s: %.2f s, tuning %+.1f cents' % (a.wav, len(x) / sr, cents), file=sys.stderr)

    lead, t, loud = lead_scores(x, sr, lo, hi, cents, octave_pen=a.octave_pen)
    path = viterbi(lead, loud, jump=a.jump)
    env, et = onset_envelope(x, sr)
    onsets, strength = detect_onsets(env, et)
    strong = [o for o, s in zip(onsets, strength) if s >= 0.15]
    notes = to_notes(path, t, lo, strong, min_note=a.min_note)
    notes = snap_starts(notes, list(onsets))
    if a.start is not None:
        notes = [n for n in notes if n[0] >= a.start - 1e-6]
    if a.end is not None:
        notes = [n for n in notes if n[0] < a.end]

    spb = 60.0 / a.tempo
    rows = []
    for s, e, m in notes:
        beats = max(0.5, round((e - s) / spb * 2) / 2)
        b = ('%g' % beats)
        rows.append("    '%5.2f  %-8s%3s'," % (s, midi_to_name(m), b))
    print('\n'.join(rows))
    print('[track] %d notes' % len(notes), file=sys.stderr)
    if a.out:
        Path(a.out).write_text('\n'.join(rows) + '\n', encoding='utf-8')

    if a.check:
        lines = library_lines(a.check)
        h, n, _ = check(notes, lines)
        print('[check] all lines: %d / %d have the draft on one of their notes' % (h, n), file=sys.stderr)
        if a.trust:
            t0, t1 = (float(v) for v in a.trust.split('-'))
            h2, n2, bad = check(notes, lines, t0, t1)
            print('[check] trusted %.1f-%.1f s: %d / %d' % (t0, t1, h2, n2), file=sys.stderr)
            for tt, ms, cur in bad[:15]:
                print('   %6.2f  written %-10s draft %s' % (tt, '+'.join(midi_to_name(m) for m in ms),
                      ' '.join(midi_to_name(m) for m in cur) or '(rest)'), file=sys.stderr)


if __name__ == '__main__':
    main()
