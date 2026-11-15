"""
check_library.py: check the notes in song-library.js against the recordings.

    python check_library.py                      # every song
    python check_library.py chura                # songs whose file name or title contains "chura"
    python check_library.py chura --all          # print every line, not only the doubtful ones

For every timed note line it measures the harmonic salience just after that time
and asks: is any note of the line among the strongest notes there? It prints the
doubtful lines (rank > --rank) with what the recording suggests instead, and a
summary per song. A doubtful line isn't always wrong (a quiet melody under a
loud band), but it is the place to listen first.
"""
import argparse
import os
import re
import sys

from musicdsp import Analysis, midi_to_name, name_to_midi

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(HERE, '..', 'REFERENCE-AUDIO-FILES')
LIBRARY = os.path.join(AUDIO_DIR, 'song-library.js')


def read_library(path=LIBRARY):
    """Parse song-library.js without a JavaScript engine: one dict per song."""
    src = open(path, encoding='utf-8').read()
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)           # block comments
    songs = []
    for block in re.split(r'\n\s*\{\s*\n', src)[1:]:
        def field(name):
            m = re.search(r'\b%s\s*:\s*\'([^\']*)\'' % name, block)
            return m.group(1) if m else ''
        nm = re.search(r'\bnotes\s*:\s*\[(.*?)\]', block, flags=re.S)
        notes = []
        if nm:
            body = re.sub(r'//[^\n]*', '', nm.group(1))         # line comments
            notes = re.findall(r"'([^']*)'", body)
        songs.append({'title': field('title'), 'audio': field('audio'), 'inst': field('inst'), 'notes': notes})
    return songs


def parse_line(line):
    """'10.16  ~G4@G+D4  0.5  label' -> (10.16, [67, 62], 0.5) ; time None when '-'."""
    parts = line.split()
    t = None if parts[0] == '-' else float(parts[0])
    body = parts[1].lstrip('~^')
    ms = [name_to_midi(tok.split('@')[0]) for tok in body.split('+')]
    beats = float(parts[2]) if len(parts) > 2 else 1.0
    return t, ms, beats


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description='Check song-library.js notes against the audio.')
    p.add_argument('filter', nargs='?', default='', help='part of a title or file name')
    p.add_argument('--rank', type=int, default=3, help='a line is doubtful if its note is not in the top N (default 3)')
    p.add_argument('--all', action='store_true', help='print every line')
    p.add_argument('--span', type=float, default=0.15)
    args = p.parse_args(argv)

    songs = [s for s in read_library() if s['audio'] and args.filter.lower() in (s['title'] + s['audio']).lower()]
    if not songs:
        print('no matching song with audio in', LIBRARY)
        return 1

    for s in songs:
        lines = [l for l in s['notes'] if l.strip()]
        parsed = [parse_line(l) for l in lines]
        timed = [(i, t, ms) for i, (t, ms, _) in enumerate(parsed) if t is not None]
        print('\n=== %s  (%s, %d notes)' % (s['title'], s['audio'], len(lines)))
        if not timed:
            print('   no timed notes: nothing to check')
            continue
        all_m = [m for _, _, ms in timed for m in ms]
        lo, hi = min(all_m) - 5, max(all_m) + 5
        a = Analysis(os.path.join(AUDIO_DIR, s['audio']), lo=lo, hi=hi)
        times = [t for _, t, _ in timed] + [a.offset + a.duration]
        ok = 0
        for k, (i, t, ms) in enumerate(timed):
            t1 = max(t + 0.07, min(times[k + 1] - 0.01, t + 0.03 + args.span))
            ranked = a.ranked(t + 0.03, t1, top=hi - lo + 1)
            order = [m for m, _ in ranked]
            rank = min(order.index(m) + 1 for m in ms if m in order)   # any note of the line (double stops, chords)
            good = rank <= args.rank
            ok += good
            if args.all or not good:
                print('   %s %6.2f  %-22s rank %-2d  strongest here: %s' % (
                    '  ' if good else '??', t, '+'.join(midi_to_name(m) for m in ms), rank,
                    ' '.join(midi_to_name(m) for m in order[:3])))
        print('   tuning %+.0f cents · %d of %d lines have a listed note in the top %d (%.0f%%)'
              % (a.cents, ok, len(timed), args.rank, 100.0 * ok / len(timed)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
