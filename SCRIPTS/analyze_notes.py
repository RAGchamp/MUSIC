"""
analyze_notes.py: find the notes in a recording and write them in the app's format.

    python analyze_notes.py ../REFERENCE-AUDIO-FILES/SONG-4-chura-liya-hai-start.wav --lo C3 --hi C6

What it does (see musicdsp.py for each step):
  1. load the WAV (mono, 22 050 Hz), optionally only --start..--end seconds
  2. STFT with long windows -> tuning offset in cents -> harmonic salience per note
  3. spectral flux with short windows -> onsets (note starts) and tempo
  4. at each onset, keep the strongest note between --lo and --hi
     (with --double-stop: the strongest pair a fourth apart, e.g. E5+B4, if both are there)
  5. drop weak readings and any --drop notes, merge quick repeats of the same note
  6. length of each note in beats (gap to the next onset / beat length, rounded to 0.5)
  7. print a report like REFERENCE-AUDIO-FILES/*-notes.txt and the lines for song-library.js

It is a FIRST DRAFT. Listen against the recording, look at weak or out-of-key notes
with inspect_time.py, fix by hand, then check the final list with check_library.py.
"""
import argparse
import os
import sys

import numpy as np

from musicdsp import Analysis, estimate_key, midi_to_name, name_to_midi


def fmt_beats(b):
    return ('%g' % b)


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description='Find the notes in a WAV file (melody line).')
    p.add_argument('wav')
    p.add_argument('--start', type=float, help='analyse from this second (times stay in file seconds)')
    p.add_argument('--end', type=float, help='analyse up to this second')
    p.add_argument('--lo', default='C4', help='lowest note to consider (default C4, above most bass/drones)')
    p.add_argument('--hi', default='A5', help='highest note to consider (default A5)')
    p.add_argument('--tuning', type=float, help='tuning offset in cents (default: measure it)')
    p.add_argument('--tempo', type=float, help='beats per minute (default: measure it)')
    p.add_argument('--double-stop', action='store_true', help='guitar: report pairs a fourth apart (E5+B4) when both sound')
    p.add_argument('--drop', default='', help='notes to ignore, comma separated, e.g. A#2,C3 (drones, known overtones)')
    p.add_argument('--weak', type=float, default=0.35, help='drop readings weaker than this x the median (default 0.35)')
    p.add_argument('--merge-gap', type=float, default=0.12, help='merge a repeat of the same note closer than this many seconds')
    p.add_argument('--delta', type=float, default=0.06, help='onset threshold above the local median (lower = more onsets)')
    p.add_argument('--min-gap', type=float, default=0.07, help='minimum seconds between onsets')
    p.add_argument('--title', help='title for the report (default: the file name)')
    p.add_argument('--out', help='also write the report to this file')
    args = p.parse_args(argv)

    log = lambda *a: print('[analyze]', *a, file=sys.stderr)
    lo, hi = name_to_midi(args.lo), name_to_midi(args.hi)
    a = Analysis(args.wav, start=args.start, end=args.end, lo=lo, hi=hi, cents=args.tuning,
                 onset_delta=args.delta, onset_min_gap=args.min_gap, log=log)
    tempo = args.tempo or a.tempo
    spb = 60.0 / tempo
    drop = {name_to_midi(n) for n in args.drop.split(',') if n.strip()}
    end_t = a.offset + a.duration

    # ---- 4. strongest note (or pair) at each onset
    found = []
    ons = list(a.onsets)
    for i, t in enumerate(ons):
        nxt = ons[i + 1] if i + 1 < len(ons) else end_t
        t0 = t + 0.03                                   # skip the noisy attack
        t1 = max(t0 + 0.04, min(nxt - 0.01, t + 0.18))  # but don't run into the next note
        v = a.notes_between(t0, t1).copy()
        for m in drop:
            if lo <= m <= hi:
                v[m - lo] = 0.0
        top = int(np.argmax(v))
        m, score = lo + top, float(v[top])
        notes = [m]
        if args.double_stop:
            # best pair (upper, upper-5 semitones); keep it only if the lower note is clearly there too
            best = None
            for k in range(5, len(v)):
                s = v[k] + v[k - 5]
                if best is None or s > best[0]:
                    best = (s, k)
            s, k = best
            if v[k - 5] >= 0.45 * v[k] and v[k] >= 0.6 * score:
                notes, score = [lo + k, lo + k - 5], float(v[k])
        found.append({'t': float(t), 'notes': notes, 'score': score, 'onset': float(a.onset_strength[i])})

    if not found:
        log('no onsets found: try a lower --delta')
        return 1

    # ---- 5. drop weak readings, merge quick repeats
    med = float(np.median([f['score'] for f in found]))
    kept = [f for f in found if f['score'] >= args.weak * med]
    log('dropped %d weak readings' % (len(found) - len(kept)))
    merged = []
    for f in kept:
        if merged and merged[-1]['notes'] == f['notes'] and f['t'] - merged[-1]['t'] < args.merge_gap:
            continue
        merged.append(f)
    log('merged %d quick repeats -> %d notes' % (len(kept) - len(merged), len(merged)))

    # ---- 6. beats
    for i, f in enumerate(merged):
        nxt = merged[i + 1]['t'] if i + 1 < len(merged) else min(end_t, f['t'] + 4 * spb)
        b = round((nxt - f['t']) / spb * 2) / 2
        f['beats'] = min(8.0, max(0.5, b))
        f['strength'] = f['score'] / med

    key = estimate_key([f['notes'][-1 if len(f['notes']) > 1 else 0] for f in merged],
                       [f['beats'] for f in merged])

    # ---- 7. report + library lines
    name = os.path.basename(args.wav)
    title = args.title or os.path.splitext(name)[0]
    t_from = a.offset
    flat = 'flat' if a.cents < 0 else 'sharp'
    pcs = {}
    for f in merged:
        for m in f['notes']:
            pcs[midi_to_name(m)[:-1]] = pcs.get(midi_to_name(m)[:-1], 0) + f['beats']
    strongest = ', '.join(k for k, _ in sorted(pcs.items(), key=lambda kv: -kv[1])[:4])

    lines = []
    lines.append('%s: notes measured from %s (%.0f s to %.0f s)' % (title, name, t_from, end_t))
    lines.append('Tuning: the recording is about %+.0f cents %s. Key: %s (strongest notes: %s).' % (a.cents, flat, key, strongest))
    lines.append('Tempo: about %.0f BPM (a beat is about %.2f s).' % (tempo, spb))
    lines.append('Method: STFT, harmonic salience per semitone (%s to %s), spectral-flux onsets. At each onset the strongest'
                 % (midi_to_name(lo), midi_to_name(hi)))
    lines.append('note was kept%s, readings weaker than %.2f x the median were dropped and repeats closer than %.2f s merged.'
                 % (' (or a double stop a fourth apart)' if args.double_stop else '', args.weak, args.merge_gap))
    if drop:
        lines.append('Ignored notes: %s.' % ', '.join(midi_to_name(m) for m in sorted(drop)))
    lines.append('This is a machine draft: check it against the recording. Strength < 0.6 = less sure.')
    lines.append('%d notes.' % len(merged))
    lines.append('')
    lines.append('  time   beats  note           strength')
    lines.append('  ------ -----  -------------  --------')
    for f in merged:
        lines.append('%7.2fs %5s  %-13s  %6.2f' % (f['t'], fmt_beats(f['beats']), ' + '.join(midi_to_name(m) for m in f['notes']), f['strength']))
    report = '\n'.join(lines)
    print(report)

    print('\n// ---- song-library.js lines ----')
    print("    key:   '%s'," % key)
    print("    tempo: %.0f," % tempo)
    print('    notes: [')
    for f in merged:
        notes = '+'.join(midi_to_name(m) for m in f['notes'])
        print("      '%6.2f  %-24s %4s'," % (f['t'], notes, fmt_beats(f['beats'])))
    print('    ]')

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            fh.write(report + '\n')
        log('report written to', args.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
