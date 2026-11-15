# SCRIPTS: finding the notes in a recording

Small Python scripts (numpy + scipy only) that Claude Code uses to turn a WAV in
`REFERENCE-AUDIO-FILES/` into note lines for `song-library.js`. They measure the sound's
frequencies over time, find where notes start, and decide which note is sounding.

Run them from this folder:

```bash
cd C:/Daya/RAGchamp/MUSIC/SCRIPTS
pip install numpy scipy        # once
```

| Script | What it does |
|---|---|
| `musicdsp.py` | The shared toolkit: load WAV, STFT, tuning offset, harmonic salience, spectral-flux onsets, tempo, key. Not run on its own. |
| `analyze_notes.py` | The whole pipeline. Prints a report like `*-notes.txt` and the lines for `song-library.js`. |
| `inspect_time.py` | The strongest notes at a few given seconds, with overtone hints, to check a doubtful reading. |
| `check_library.py` | Checks every timed line in `song-library.js` against its recording and lists the doubtful ones. |

## Typical session for a new song

```bash
# 1. first draft (melody between C4 and A5; times are seconds in the file)
python analyze_notes.py ../REFERENCE-AUDIO-FILES/SONG-6-xyz-start.wav --lo C4 --hi A5 --out draft.txt

#    guitar intro with double stops on the e and B strings, ignoring a low Bb drone
python analyze_notes.py ../REFERENCE-AUDIO-FILES/SONG-1-inteha-ho-gayi-start.wav --lo E4 --hi G5 --double-stop
python analyze_notes.py ../REFERENCE-AUDIO-FILES/SONG-4-chura-liya-hai-start.wav --lo C3 --hi C6 --drop A#2

# 2. look closer at doubtful notes (strength < 0.6, out of key, octave jumps)
python inspect_time.py ../REFERENCE-AUDIO-FILES/SONG-4-chura-liya-hai-start.wav 6.22 11.42

# 3. fix by hand, paste into song-library.js, then check the final list
python check_library.py chura
```

Useful options of `analyze_notes.py`:

| Option | Default | Use it when |
|---|---|---|
| `--start / --end` | whole file | only part of the clip matters |
| `--lo / --hi` | C4 / A5 | the melody sits elsewhere; keep the bass or drone out |
| `--drop A#2,C3` | none | a drone or a known overtone keeps winning |
| `--double-stop` | off | guitar parts played as pairs a fourth apart (E5+B4) |
| `--tempo 150` | measured | the measured tempo is half or double (the log lists other candidates) |
| `--tuning -28` | measured | you already know the offset |
| `--delta 0.04` | 0.06 | soft playing: notes are missed (lower = more onsets) |
| `--weak 0.5` | 0.35 | too many ghost notes |
| `--merge-gap 0.2` | 0.12 | repeated notes are split into too many boxes |

## How each step works

1. **Load:** read the WAV, mix to mono, scale to -1..+1, resample to 22 050 Hz.
2. **STFT** (4096-sample Hann windows, about 0.19 s, every 256 samples): how strong each frequency is over time.
3. **Tuning:** exact frequency of the spectral peaks (parabolic fit) against the nearest note, as a
   loudness-weighted circular mean in cents. Old film recordings are often 10–40 cents flat.
4. **Harmonic salience:** each note's score = its energy + 0.8 × 2nd harmonic + 0.8² × 3rd … (6 harmonics),
   so the real note beats its own overtones.
5. **Onsets:** spectral flux (1024-sample windows): the summed *increase* in log magnitude between frames.
   Peaks above the local median + `--delta`, at least `--min-gap` apart, are note starts.
6. **Pick and clean:** the strongest note 0.03–0.18 s after each onset; drop weak ones; merge quick repeats.
7. **Tempo and beats:** autocorrelation of the flux with a comb over 1–4 beats → BPM;
   each gap to the next note ÷ beat length, rounded to ½ beat.
8. **Key:** Krumhansl-Kessler profiles on the notes found, weighted by length.

## Limits

- Melody line only: one note (or one double stop) per onset, not full chords.
- Loud, busy accompaniment can win over a quiet tune; octaves are not always certain.
- Tempo is ambiguous (half or double speed fit too); check it and pass `--tempo`.
- The output is a draft. Listen against the recording and fix it by hand. `check_library.py`
  shows where to listen first.

## Check results on the current library (2026-11-15)

`python check_library.py`, a line counts as OK when one of its notes is in the 3 strongest:

| Song | Measured tuning | Lines OK |
|---|---|---|
| Inteha Ho Gayi | −11 cents | 63 / 68 (93%) |
| Tip Tip Barsa Pani | −18 cents | 93 / 93 (100%) |
| Pehla Nasha | −14 cents | 186 / 186 (100%) |
| Chura Liya Hai | −35 cents | 81 / 82 (99%) |
| Anhoni Ko Honi | −44 cents | 123 / 141 (87%) |
