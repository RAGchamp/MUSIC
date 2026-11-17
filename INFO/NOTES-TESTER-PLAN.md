# Notes Tester: plan

**Status:** approved and built (2026-11-15): `NOTES-TESTER/index.html`. Open questions answered (see section 11).
Built as planned, except: the synth is rendered in 4 s chunks without a compressor (much faster), re-strikes of the
note already sounding are counted rather than listed as MISSING, and Compare takes ~3–12 s on the owner's PC, not under 2 s.
The optional `INFO/HOW-MUSIC-APP-WORKS.html` section was not added.

## 1. Goal

A second page, `NOTES-TESTER/index.html`, that checks whether the note lines in
`REFERENCE-AUDIO-FILES/song-library.js` really match the recordings:

1. **Choose a song.** All of its notes are tested.
2. **▶ Test notes:** synthesise audio from the song's note lines and play it. The original
   recording is **not** played.
3. **⬇ Download WAV:** save the synthesised audio as a stereo `.wav` file.
4. **🔍 Compare audio files:** compare the synthesised audio with the original recording and
   write the result for every note line into a text box.
5. **📋 Copy:** copy that report so it can be pasted into Claude Code, which then updates the notes
   in `song-library.js`.

## 2. What "no difference" can and can't mean (important)

A synthesised piano/guitar/accordion will never be **sample-for-sample** the same as a film
recording: the timbre, the reverb, the accompaniment, the singer and the tape tuning all differ.
A waveform diff would always report "100 % different", even with perfect notes.

So the comparison is **musical**, not a waveform diff. For each note line it asks:

| Question | How |
|---|---|
| Is the written **pitch** what the recording plays at that moment? | Harmonic salience of every note in the window after the note's start, in the original. Pass when a written note is among the 3 strongest. |
| Is the written **start time** right? | Nearest note onset (spectral flux) in the original, within ±80 ms. |
| Is there a **missing** note? | A strong onset in the original with no note line within ±80 ms. |
| Is there an **extra** note? | A note line with no onset near it and a pitch that isn't sounding. |
| Does the **timeline** line up overall? | Per-window chroma (12 pitch classes) of the synth vs. the original, as a similarity score 0–1. |

"No difference" therefore means: every line passes the pitch and time checks and no missing
notes are found. This is the same idea as `SCRIPTS/check_library.py`, moved into the browser and
extended with onset checks, so it works on GitHub Pages without Python.

The same analysis is also run on the **synthesised** audio as a control. If the analyser can't read
the written notes back from the synth, the problem is the analyser (or the synth), not the notes,
and the report says so instead of blaming the notes.

## 3. Files

| Path | Change |
|---|---|
| `NOTES-TESTER/index.html` | **New.** The whole tester in one file (HTML + CSS + JS, Bootstrap 5.3.3 from jsDelivr, no build step), like the main app. |
| `index.html` | Footer: add a link `🧪 Notes Tester` next to `🎙️ Record or trim a song`. |
| `.claude/CLAUDE.md` | Add the new page to the file table and a short section on how it works. |
| `INFO/HOW-MUSIC-APP-WORKS.html` | Optional: a short "Checking the notes" section. |
| `INFO/NOTES-TESTER-PLAN.md` | This plan. |

The tester reads the existing data; it doesn't change any of it:

- `../REFERENCE-AUDIO-FILES/song-library.js` via `<script src>` (works on `file://` and Pages).
- `../SONG-INSTRUMENT.json` via `fetch()`, falling back to the song's `inst` field on `file://`, as the main app does.
- `../logo.svg` in the nav.

## 4. UI (same look as `index.html`)

Same sticky deep-blue nav with `logo.svg` and the tagline, the same `.step-card` cards with yellow
step numbers, the same colours, a pink `.about-box` at the top explaining the page, and the same
footer. Phone (390 px) and laptop (1280 px) layouts both work.

```
┌ nav: logo ─────────────────────────────── Music Practice App ┐
│ [pink box] What the Notes Tester does … Back to practice →    │
│ 🧪 Notes Tester                                               │
│ ┌ 1 Choose a song ─────────────────────────────────────────┐  │
│ │ [song drop-down]   🎸 Guitar · E minor · 68 notes · file  │  │
│ └──────────────────────────────────────────────────────────┘  │
│ ┌ 2 Test notes ────────────────────────────────────────────┐  │
│ │ [▶ Test notes] [■ Stop] [⬇ Download WAV]  progress bar    │  │
│ │ Now playing: E5+B4                                        │  │
│ │ #1  0.61  E4+B3+G3+E3+B2+E2  2  Em chord                  │  │
│ │ #2  1.43  B4+F#4             0.5   ← current row yellow   │  │
│ │ …  (read-only scrolling list, one row per note line)      │  │
│ └──────────────────────────────────────────────────────────┘  │
│ ┌ 3 Compare audio files ───────────────────────────────────┐  │
│ │ [🔍 Compare audio files]  [📋 Copy report]                 │  │
│ │ summary pills: 61/68 OK · 5 pitch · 2 timing · 3 missing  │  │
│ │ ┌ textarea (monospace, read-only, ~20 rows) ──────────┐   │  │
│ │ │ report …                                            │   │  │
│ │ └─────────────────────────────────────────────────────┘   │  │
│ └──────────────────────────────────────────────────────────┘  │
└ footer ───────────────────────────────────────────────────────┘
```

- The note list in step 2 is read-only (no checkboxes): it shows what is being played. Clicking a
  row plays that one note, as clicking a note box does in the main app.
- After Compare, each row in the list also gets a small coloured verdict badge (green OK, orange
  flagged), so problem notes are easy to spot by eye as well as in the text box.

## 5. Generating the audio (Test notes)

- Render with an **`OfflineAudioContext`** rather than live: the result is an exact `AudioBuffer`
  that is both played and downloaded, and is identical every time.
- Reuse the main app's sound code (`tone()`, `osc()`, `ksBuffer()`): triangle + sine for piano,
  Karplus-Strong for guitar, detuned sawtooths for accordion, chosen from the song's instrument.
  It is copied into the tester (the project has no shared JS files; copying keeps both pages
  standalone, as the main app already did with the BLOG composer).
- **Timing:** the render starts at 0 s and is as long as the original recording, and each note starts
  at its written `time`. So the synth lines up with the original second for second, and a time in the
  downloaded file is the same time in the original. A note lasts until the next line's time (or
  `beats × 60 / tempo` for the last note, or when the times are `-`).
- Slides (`~`) and hammer-ons (`^`) use the same `from` / `soft` / `tie` options as the main app.
- Every note of a line (e.g. both notes of `E5+B4`, all six of a chord) is sounded.
- **Tuning:** an optional "Match recording tuning" box shifts the synth by the measured offset
  (e.g. −11 cents for Inteha), so the synth sounds in tune with the original when compared by ear.
- Format: **48 000 Hz stereo** (the same as the recordings). The synth is mono, so both channels
  are the same.
- **Playback:** an `AudioBufferSourceNode` plays the buffer; a `requestAnimationFrame` loop turns
  the current row yellow, as in the main app. Space plays or stops.

## 6. Download WAV

- Encode the buffer as **16-bit PCM stereo, 48 kHz** WAV in JS (44-byte header + interleaved
  samples), make a `Blob` and download it through an `<a download>` link. Same format as the
  files in `REFERENCE-AUDIO-FILES/`.
- File name: `<audio name>-from-notes.wav`, e.g. `SONG-1-inteha-ho-gayi-start-from-notes.wav`.
- It goes to the browser's Downloads folder (no folder picker needed).

## 7. Compare audio files

### 7.1 Getting the original

- On GitHub Pages or a local server: `fetch('../REFERENCE-AUDIO-FILES/<file>')` then
  `decodeAudioData()`.
- On `file://` the browser blocks `fetch()`. The page then shows a **"Choose the original WAV"**
  file picker (a plain single-file `<input type="file">`, not a folder scanner) pre-labelled with
  the expected file name, and checks that the chosen file's name matches.

### 7.2 Analysis (all in JS, ported from `SCRIPTS/musicdsp.py`)

Both signals are mixed to mono and resampled to 22 050 Hz, then:

1. **STFT:** 4096-sample Hann window, hop 256, radix-2 FFT written in plain JS (no library).
2. **Tuning offset** of the original: parabolic peak fit, loudness-weighted circular mean in cents.
3. **Harmonic salience** per MIDI note (6 harmonics, decay 0.8, ±35 cents), in the
   window 0.03–0.18 s after each note's start, as `analyze_notes.py` does.
4. **Onsets:** spectral flux (1024 window, hop 128), median + delta peak picking.
5. **Chroma** per note window for the synth vs. original similarity.

Speed target: under 2 s for the longest clip (Pehla Nasha, 73 s). The work is done in chunks with
`await` between them, and a progress message shows, so the page doesn't freeze.

### 7.3 Verdict for each line

| Verdict | Rule |
|---|---|
| `OK` | A written note is in the original's 3 strongest **and** an onset is within ±80 ms. |
| `PITCH?` | No written note in the 3 strongest. The report gives the strongest notes heard. |
| `OCTAVE?` | The right pitch class but another octave is stronger. |
| `TIME?` | Pitch OK but the nearest onset is 80–250 ms away. The report gives the measured time. |
| `EXTRA?` | No onset within 250 ms and the pitch isn't sounding. |
| `MISSING` | (between lines) a strong onset in the original that no line covers. |

Thresholds: **top 3 and ±80 ms** (confirmed). They are constants at the top of the script, so they
are easy to change later.

### 7.4 The report (text box)

Plain text, written so it can be pasted straight into Claude Code. It names the song and file, gives a
summary, then **every line** in order (OK lines too), with `MISSING` rows inserted where they fall in
time. Each flagged line has a suggested replacement in `song-library.js` format; OK lines show `-` in
that column. A final "Lines to fix" list repeats just the flagged line numbers so they are easy to find
in a long report (e.g. 186 lines for Pehla Nasha).

```
NOTES TESTER REPORT
Song:        Inteha Ho Gayi: guitar intro (Sharaabi)
Audio file:  REFERENCE-AUDIO-FILES/SONG-1-inteha-ho-gayi-start.wav
Instrument:  guitar      Tuning of recording: -11 cents
Lines tested: all 68 (0.61 s – 21.90 s)
Result:      61 OK · 3 PITCH? · 2 TIME? · 1 OCTAVE? · 0 EXTRA? · 2 MISSING
Synth vs original chroma similarity: 0.87
Control (synth read back): 68/68 OK

#   time   written            verdict   heard (strongest first)      onset   suggested line
1   0.61   E4+B3+G3+E3+B2+E2  OK        E4 1.00, B3 0.81, G3 0.64     0.61    -
2   1.43   B4+F#4             OK        B4 1.00, F#4 0.77, B3 0.30    1.44    -
…
14  6.01   G5+D5              PITCH?    F#5 0.92, C#5 0.71, E5 0.40   6.02    ' 6.01  F#5+C#5   0.5'
…
22  8.32   ~B4+F#4            TIME?     B4 1.00, F#4 0.83             8.21    ' 8.21  ~B4+F#4   0.5'
…
40  12.70  E4                 OCTAVE?   E5 1.00, E4 0.55              12.70   '12.70  E5        0.5'
--  14.05  (no line)          MISSING   D5 0.88, A4 0.66              14.05   '14.05  D5+A4     0.5'
…

Lines to fix: 14, 22, 40, … and missing notes at 14.05 s, …
Notes for Claude Code: update these lines in REFERENCE-AUDIO-FILES/song-library.js
(song "Inteha Ho Gayi…"), then run SCRIPTS/check_library.py inteha and the Notes Tester again.
```

### 7.5 Workflow with Claude Code

1. Run the tester, press **Compare**, press **📋 Copy report**.
2. Paste into Claude Code: "update the notes from this report".
3. Claude Code edits `song-library.js` (and can confirm with `inspect_time.py` at the listed times).
4. Reload the tester and compare again until the report is clean or the rest are known false alarms.

## 8. Testing

- Open `NOTES-TESTER/index.html` from disk (file picker path) and from a local server / Pages (fetch path).
- Headless Chrome via a Node CDP script (`--autoplay-policy=no-user-gesture-required --mute-audio`) to check:
  the render produces a buffer as long as the original, the WAV header is valid stereo 48 kHz 16-bit,
  the yellow row moves forward, and Compare finishes and fills the text box for all 5 songs.
- **Sanity checks on the analyser:**
  - synth compared with itself → every line `OK`;
  - deliberately wrong notes (shift one line by a tone, move one by 0.3 s) → those lines flagged;
  - results on the real songs roughly match `check_library.py` (93 %, 100 %, 100 %, 99 %, 87 %).
- Screenshots at 390 px and 1280 px.

## 9. Build order

1. Page shell: nav, pink box, the 3 step cards, footer; load the song library and instrument.
2. Read-only note list in step 2.
3. Offline render + playback + yellow row.
4. Stereo WAV download.
5. JS DSP port (FFT, STFT, tuning, salience, onsets, chroma), checked against the Python numbers.
6. Compare + full report + verdict badges + copy button.
7. Footer link in `index.html`, CLAUDE.md, optional INFO page section.
8. Tests and screenshots, then a commit. **Ask before pushing.**

## 10. Out of scope / limits

- The tester never edits `song-library.js` itself; Claude Code does that from the report.
- No picking of individual note lines: the whole song is always tested.
- Melody check only, as with the Python scripts: loud accompaniment can hide a quiet note, so some
  `PITCH?` and `MISSING` items will be false alarms. The report flags; you judge by ear.
- No AI runs in the page; the comparison is plain signal processing.

## 11. Decisions (answered 2026-11-15)

| Question | Decision |
|---|---|
| What to choose before testing | **Song only.** All of the song's notes are tested; no per-line checkboxes. |
| Downloaded WAV format | **Stereo**, 16-bit, 48 kHz, same as the recordings. |
| What the report lists | **Every line**, plus a "Lines to fix" summary at the end. |
| Pass thresholds | **As planned:** a written note in the 3 strongest, start within ±80 ms. |
