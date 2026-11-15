"""
inspect_time.py: what is sounding at a few moments of a recording?

    python inspect_time.py ../REFERENCE-AUDIO-FILES/SONG-4-chura-liya-hai-start.wav 6.22 11.42 21.77

For each time it prints the strongest notes (harmonic salience, strongest first)
and the onsets found nearby. Use it to check a doubtful reading from
analyze_notes.py: e.g. a G5 that is really the 3rd harmonic of a C4, or an
octave that could go either way.
"""
import argparse
import sys

import numpy as np

from musicdsp import Analysis, midi_to_hz, midi_to_name


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description='Show the strongest notes at given times.')
    p.add_argument('wav')
    p.add_argument('times', type=float, nargs='+', help='seconds in the file')
    p.add_argument('--lo', default='C3')
    p.add_argument('--hi', default='C6')
    p.add_argument('--span', type=float, default=0.15, help='seconds after each time to average over (default 0.15)')
    p.add_argument('--top', type=int, default=6)
    p.add_argument('--tuning', type=float)
    args = p.parse_args(argv)

    a = Analysis(args.wav, lo=args.lo, hi=args.hi, cents=args.tuning,
                 log=lambda *m: print('[inspect]', *m, file=sys.stderr))
    for t in args.times:
        ranked = a.ranked(t + 0.03, t + 0.03 + args.span, top=args.top)
        best = ranked[0][1] or 1.0
        near = [o for o in a.onsets if abs(o - t) <= 0.3]
        print('\n%.2f s   onsets nearby: %s' % (t, ', '.join('%.2f' % o for o in near) or 'none'))
        print('   note   Hz       score   relative')
        for m, s in ranked:
            bar = '#' * int(round(20 * s / best))
            print('   %-5s %7.1f  %7.3f   %4.2f  %s' % (midi_to_name(m), midi_to_hz(m, a.cents), s, s / best, bar))
        # among the 3 strongest: is one an overtone of another (lower) one?
        for m_hi, _ in ranked[:3]:
            for m_lo, _ in ranked[:3]:
                h = 2 ** ((m_hi - m_lo) / 12.0)
                for n in (2, 3, 4, 5):
                    if m_lo < m_hi and abs(12 * np.log2(h / n)) < 0.3:
                        print('   note: %s could be the %s harmonic of %s' % (
                            midi_to_name(m_hi), {2: '2nd', 3: '3rd', 4: '4th', 5: '5th'}[n], midi_to_name(m_lo)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
