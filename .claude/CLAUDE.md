# Music Practice App

A single-page web app for practising songs. Pick a song, choose **Piano** or **Guitar**, press **Play**:
the song's **original recording** plays, and the note being played is highlighted in yellow on
the keyboard, or on the fretboard and tab, and in the note boxes.

The owner uses it for personal learning.

- **Live site:** https://ragchamp.github.io/MUSIC/ (GitHub Pages, served from `main`, root folder)
- **Repo:** https://github.com/RAGchamp/MUSIC (public)
- **Local folder:** `C:\Daya\RAGchamp\MUSIC` (it used to be called `MUSIC-MODEL`, and the page used to be `SONG-PRACTICE.html`)
- **Sister project:** `C:\Daya\RAGchamp\BLOG\MUSIC-BASICS.html` (repo RAGchamp/BLOG). This app was cut down from that page's
  composer, so its audio engine, fretboard and tab code started as copies of it.

## Files

| Path | What it is |
|---|---|
| `index.html` | The whole app: HTML, CSS and JS in one file. Bootstrap 5.3.3 comes from the jsDelivr CDN; there is no build step. |
| `recorder.html` | Records another browser tab's audio (`getDisplayMedia`) to a 16-bit WAV and saves it in a chosen folder (File System Access API; the folder handle is remembered in IndexedDB). It also trims a file: it copies start–end seconds into `name-copy-<timestamp>.wav` in the same folder. It is linked from the index.html footer. |
| `SONG-INSTRUMENT.json` | Each song's instrument (`piano`, `guitar` or `accordion`), keyed by audio file name. Every song in the library needs an entry. |
| `logo.svg` | The logo in the top nav (a copy of the BLOG logo). |
| `REFERENCE-AUDIO-FILES/song-library.js` | **The song list.** It defines `window.SONG_LIBRARY`, which fills the song drop-down. |
| `REFERENCE-AUDIO-FILES/*.wav` | Song recordings, e.g. `SONG-1-inteha-ho-gayi-start.wav` (22 s, 4 MB). |
| `REFERENCE-AUDIO-FILES/SONG-1-inteha-ho-gayi-notes.txt` | Old analysis notes. Its times come from an **earlier** recording and **do not** match the current WAV. The app doesn't use it. |
| `readme` | The original one-line readme from GitHub. |
| `SCRIPTS/` | Note-analysis scripts (numpy + scipy): `analyze_notes.py` drafts note lines from a WAV, `inspect_time.py` shows the strongest notes at given seconds, `check_library.py` checks `song-library.js` against the recordings, `musicdsp.py` is the shared toolkit. See `SCRIPTS/README.md`. |
| `INFO/HOW-MUSIC-APP-WORKS.html` | Explainer page: recorder, note analysis, AI's role, the practice UI, highlight, single-note sounds. |
| `NOTES-TESTER/index.html` | **Notes Tester**: plays a song's notes as synth audio (never the recording), downloads it as a WAV, and compares the notes with the original recording, writing a per-line report to paste into Claude Code. Linked from the index.html footer. See "Notes Tester" below. |
| `INFO/NOTES-TESTER-PLAN.md` | The approved plan for the Notes Tester. |
| `NOTES-TESTER/WAV-VISUALIZER.html` | **WAV Visualizer**: the notes found in two WAVs of one song (the original and a Notes Tester file) as coloured boxes side by side, with differences outlined. Linked from both footers and the Notes Tester's step 3. See "WAV Visualizer" below. |
| `INFO/WAV-VISUALIZER-PLAN.md` | The approved plan for the WAV Visualizer, with the owner's decisions. |
| `NOTES-TESTER/Piano-tester.html` (was Piano.html) | **Piano Capture**: an 88-key piano that writes key strokes as song-library.js lines with times in the WAV, played by hand (laptop keys, optionally along with the WAV) or found in a WAV. See "Piano Capture" below. |
| `contactus.html` | **Contact Us** (adapted from BLOG/contactus.html): LinkedIn/email buttons, About Me, the owner's three passions (music, software, AI), why AI for learning music, cards linking every page of the app, "Built entirely with Claude Code" (what the owner did vs what Claude Code did), how others can use and build on it, an accuracy note. Linked from the index.html and piano.html footers. |
| `piano.html` | **Piano demo** (site root; linked from index.html as "🎹 Try our Piano player" under the pink box and in the footer): nav, pink "How does the RAG Champ Piano app work?" box, one **▶ Try it** button that shows two song buttons (🎼 Für Elise, 🎬 Bollywood: Pehla Nasha), then the Piano Notes Player playing the chosen one. Built by a script from `NOTES-TESTER/Piano-notes.html` with `SONG-6-FUL-ELISE-BEETHOVEN.txt` and `SONG-3-PEHLA-NASHA-ORGIG-NOTES-5MIN.txt` embedded in `<script type="text/plain" id="demoFur">` / `id="demoPehla"` (so it works from disk) and samples from `NOTES-TESTER/SAMPLES/piano.js`; rebuild it after changing the player. |
| `mini-piano.html` | **Mini Piano** (site root, made for phones): one octave C5–C6 of big keys; Manual (tap) and Automated (table of key + wait ms, ▶ Play) modes. See "Mini Piano" below. Linked from the index.html, piano.html and contactus.html footers and a contactus card. |
| `MUSIC-THEORY/MUSIC-BASICS-TEST-1.html` | **Music Basics Test 1** (2026-11-18): 25 multiple-choice questions on MUSIC-BASICS.html, each with a mini piano to hear every option. See "Music Basics Test" below. Linked from the Music Basics page (end of Part D and footer), SITE-MAP.html and contactus.html. |
| `INFO/MUSIC-THEORY-TEST-APP-PLAN.md` | The approved plan for the Music Basics Test, with the owner's decisions. |
| `INFO/MINI-PIANO-PLAN.md` | The approved plan for the Mini Piano, with the owner's decisions. |
| `INFO/HOW-PIANO-NOTES-PLAYER-WORKS.html` | Explainer (same look as HOW-MUSIC-APP-WORKS.html): part 1 how Piano-notes.html works (loading, hand split, fingering, taps vs black-key reaches, sound, score sync, bar ranges); part 2 how the Pehla Nasha PDF became the 5-minute notes file. |
| `NOTES-TESTER/Piano-notes.html` | **Piano Notes Player**: plays a notes file (or a song-list song) on the piano samples with two animated hands pressing the keys (numbered fingers) and the score scrolling in a frame below. See "Piano Notes Player" below. |
| `S-PAD/MUSIC-NOTES/*.html` | **Retired** (moved 2026-11-17, git-ignored): the old sheet music pages made from WAV analysis and web searches. Nothing uses them. See "How new songs are made". |
| `MUSIC-THEORY/MUSIC-BASICS.html` | **Music Basics** (beginner theory, added 2026-11-17; copied from BLOG's MUSIC-BASICS.html, nav/footer now point to `../`): Western & Indian basics, a composer app, and **Part D** (sections 13–20): 39 short theory lessons in 8 groups (The Basics, Rhythm and Meter, Scales and Key Signatures, Intervals, Chords, Diatonic Chords, Chord Progressions, Neapolitan Chords) with a lesson index. The owner removed the Tip Tip and Inteha song presets. Part D helpers: `.mstaff` (data-clef/key/time/notes, drawn by `drawStaff()`; tokens `C4+E4/q.@label`, `r/h`, `|`, `||`, `|.`, `~`), 🔊 `data-play="C4:1 C4+E4+G4:2 r:1"` (`playTokens`, `data-bpm`), `data-meter="2+2+3"` (`playMeter`), key-signature calculator (15.5). Its note parser is `pdNote` (the composer already has a `parseNote`). |
| `MUSIC-PROD/SONG.html` | **Dil Tera Pighla Doon** (2026-11-19): the owner's original Hindi song (lyrics and music by Daya, AI voice; `MUSIC-PROD/Dil-Tera-Pighla-Doon-with-tabla.wav`, 3:09, 36 MB). Red jukebox (Play/Pause/Stop, progress bar; no autoplay, the browser blocked it), pink credit box ("Daya" links to contactus.html in a new tab), a black SVG box: spinning flowers, drifting shapes and orbiting dots; a dark side-on woman's silhouette with flowing hair on a green glow blurs in at 0:40 and out at 2:20 (`SHOW_IN`/`SHOW_OUT`, follows `audio.currentTime`); green lyrics box with section times (the part being sung lights up) and an English translation. Linked from the end of Music Basics (creativity box + footer) and SITE-MAP.html. Everything else from MUSIC-PROD (other WAVs, lyric drafts) was moved to the git-ignored `S-PAD/`. |
| `MUSIC-PROD/SONG-2.html` | **Rani Rani** (2026-11-20): the owner's fast English dance song (boy-band pop with a Raï flavour; lyrics from SONG-LOGIC/SONG-2-RANI-RANI-ENGLISH-LOGIC.html) (`MUSIC-PROD/Rani-Rani.wav`, 3:52, 44 MB). Same jukebox/pink/green boxes as SONG.html; the black box is a disco stage with an always-glowing neon green "RANI RANI" sign and two big SVG monkeys in red velvet suits (`#velvet` gradient, sleeves and trousers too), yellow shoes and green caps (Chiku waves a banana; Miku has a pink flower on her cap; she is drawn mirrored), with pink/red hearts floating up behind everything (`hearts`, positions as fractions of the stage, pulse on the beat) changing dance move every 16 half-beats (clap, wave, scratch, punch, swim). The six small characters were replaced 2026-11-20 because they looked tiny in the owner's portrait video: the viewBox now follows the box's shape (`layout()`, ResizeObserver; phones use a 4:5 box) so the monkeys fill it. They dance on the measured beat (`BEAT` = 60/192 s, `PHASE` 0.208 s) and harder when louder (`ENERGY`, one digit 0–9 per second). English lyrics, no translation; only the intro (0:00–0:33) and ending (3:42–) have times. Linked from Music Basics (creativity box + footer) and SITE-MAP.html. |
| `SONG-LOGIC/*.html` | Song plans (same look as the old S-PAD notes pages): `SONG-1-RANI-RANI-LOGIC.html` (Hindi Raï-pop, adapted from the style of Khaled's "Didi"), `SONG-2-RANI-RANI-ENGLISH-LOGIC.html` (English, late-90s boy-band style), `SONG-3-LAILA-LAILA-LOGIC.html` (Mehbooba-style music, Boney M-style English vocals), `SUNO-GUIDE.html` (how to use suno.com). Pages 2 and 3 have a 📋 Copy all button for the Suno inputs. Not linked from the main pages yet. |

## Why the song list is a .js file

A browser page can't list the files in a folder, and on `file://` it can't `fetch()` JSON either. A `<script src>`
works in both places (opened from disk and on GitHub Pages), so songs are listed in `song-library.js`.
The owner asked for the "Scan folder" button (a `webkitdirectory` file picker) to be **removed**. Don't add it back.

## song-library.js format

```js
window.SONG_LIBRARY = [
  {
    title: 'Inteha Ho Gayi: guitar intro (Sharaabi)',
    audio: 'SONG-1-inteha-ho-gayi-start.wav',   // file in REFERENCE-AUDIO-FILES (case-sensitive on GitHub Pages!)
    key:   'E minor',                            // shown under the picker
    inst:  'guitar',                             // fallback instrument when SONG-INSTRUMENT.json can't be read (file://)
    // wavTag: 'v2',                             // optional: only for an entry that shares its recording with another
    tempo: 154,                                  // only used when the notes have no times
    notes: [
      // 'time   notes   beats   label'
      ' 0.61  E4+B3+G3+E3+B2+E2        2  Em chord',
      ' 2.10  ~E5+B4                   1',
      '10.16  G4@G                   0.5',
    ]
  }
];
```

Note lines are parsed by `parseLine()` in index.html:

- **time:** the second in the audio file where the note starts. Use `-` if the song has no timings; the timeline is then built from beats × tempo.
  The highlight follows `audio.currentTime` against these times.
- **notes:** names joined by `+`, written `C4`, `F#4`, `Bb3` (`♯` and `♭` also work). The first name is the main note.
  - `~` in front means a slide into the note; `^` means a hammer-on or pull-off.
  - `@string` (one of `e B G D A E`) forces a note onto a string. Otherwise the note goes on the lowest fret of a free string (`placeOnGuitar`).
  - Most Inteha notes are double stops: the same fret on the e and B strings, e.g. `E5+B4` is fret 12.
- **beats:** the note's length, which sets the width of its tab column and note box.
- **label:** optional text shown instead of the note names, e.g. `Em chord`.

To **add a song**:
1. Copy the WAV into `REFERENCE-AUDIO-FILES/`.
2. Add an entry to `song-library.js`.
3. Add an entry to `SONG-INSTRUMENT.json`: `{ "audio": "<wav name>", "title": "...", "instrument": "piano" | "guitar" | "accordion" }`.
   Use the same instrument as the song's `inst` field. `accordion` uses the piano keyboard view
   (a piano accordion's right hand is a piano-style keyboard) with its own reed sound.
4. Commit and push.

A song with no `audio` can't be played: the Play button is disabled.

The Inteha timings (68 notes) came from pitch and onset analysis of the clip with numpy/scipy:
STFT, a double-stop salience score, spectral-flux onsets, and a tuning offset of about −10 cents.
They were then cleaned up by hand against the owner's tab.

## How the page works (index.html)

1. **Choose a song:** `#songSel` lists `library`. Choosing one shows the key, the note count and the file name in `#songMeta`.
2. **Instrument:** there is **no instrument picker**; the owner asked for it to be removed. Choosing a song goes straight to
   practice on that song's instrument (`instrumentFor()`), shown as 🎸 Guitar, 🎹 Piano or 🪗 Accordion in `#songMeta` (`INST_LABEL`).
   Accordion uses the keyboard view; everywhere the code branches, it is `inst === 'guitar'` vs. not.
   - The instrument comes from `SONG-INSTRUMENT.json`, matched by the audio file name.
   - On `file://` the page can't `fetch()` the JSON, so it falls back to the song's `inst` field in song-library.js.
     **Keep the two the same.** A song in neither defaults to piano.
3. **Practice** (`buildPractice()`):
   - **Piano:** `buildKeyboard()` draws keys from C ≤ the lowest note (at least C3) up to C ≥ the highest note (at least C6). Keys the song uses are green.
   - **Guitar:**
     - `buildFretboard()`: 6 strings × open + 15 frets. Positions the song uses are green dots, and position-marker dots are drawn like a real neck.
     - `buildTab()`: one column per note. The top line shows `/` `\` `h` `p` or the label.
   - `buildChips()`: the note boxes. Guitar boxes show "fret N" plus the note names; piano boxes show the note names. Purple badges mark slides and hammer-ons/pull-offs.
   - **Now playing / Next** cards (`describe()`): note names, plus string and fret details on guitar.
   - **Controls:** ▶ Play, ■ Stop, Speed 50–125% (`audio.playbackRate`, `preservesPitch`), 🔁 Loop, progress bar, and <kbd>Space</kbd> to play or stop.

### Playback

- **Play only ever plays the original recording** (`playRecording()` uses `new Audio(...)`). The owner asked for the
  Sound selector and synth playback to be **removed**; don't add them back.
- `tick()` is a `requestAnimationFrame` loop. It finds the last note whose time is ≤ `audio.currentTime` and calls `highlight(i)`, which:
  - adds `.playing` to the note box, the keys or the fret cells, and the tab column;
  - fades notes already played (`.done`);
  - keeps the note box area, the tab and the keyboard scrolled to the current note.
- If the audio can't load, the prompt says which file is missing.

### Single-note sounds

Clicking a note box, a key or a fret calls `hear()` / `tone()`. This is the only synth sound left:
- piano is a triangle plus sine oscillator;
- guitar is a Karplus-Strong plucked string (`ksBuffer`) through a small body EQ;
- accordion is two slightly detuned sawtooths (musette beat) through a low-pass, with a soft bellows attack.

### Responsive fretboard

- The fretboard is **one CSS grid**. Every label and cell stores its laptop-layout place in `data-r`/`data-c`.
- `layoutFretboard()` places the pieces. When `matchMedia('(max-width: 767.98px)')` matches, it turns the board **90° anticlockwise**:
  - `gridRow = 18 − c`, `gridColumn = r`;
  - open strings at the bottom, fret 15 at the top, strings left to right e B G D A E;
  - class `.vertical` swaps the fret wires to `border-top`, makes strings vertical lines and moves the position markers.
- It re-runs when the screen size changes. Laptop layout: horizontal, `min-width:760px`, scrolls sideways if it has to.

### Look and feel

- **Top nav:** the same as the BLOG site: sticky, deep blue `#04264d`, yellow `#ffd60a`, `logo.svg` on the left, and the tagline **"Music Practice App"** on the right.
- **Step boxes:** cards with a **uniform** 2px `#c9d3e3` border (`.step-card`). The owner asked for the coloured left accent lines to be removed.
- **Highlight colour:** yellow `--biz-yellow` (#ffc107).
- **Pink "How this App works and how AI plays a part?" box** (`.about-box`) at the top of `<main>`, under the nav:
  a ~400-character summary of `INFO/HOW-MUSIC-APP-WORKS.html` and a **Learn more →** link to it.

## Notes Tester (NOTES-TESTER/index.html)

One self-contained page, same look as index.html (nav, pink box, step cards). It loads
`../REFERENCE-AUDIO-FILES/song-library.js` and `../SONG-INSTRUMENT.json`, and never edits them.

1. **Choose a song:** the whole song is always tested (the owner chose no per-line selection).
   **Notes from: song list / text file** (`#srcSel`). The "sheet music" option (it read `MUSIC-NOTES/*-notes.html`) was
   removed on 2026-11-17 together with that folder.
   **Notes from: text file** (`txtSong`, added 2026-11-16) takes any .txt through a file picker: song-library.js note lines
   (quotes, trailing commas and `//` comments ignored; unreadable lines are listed and skipped). `tempo: N` and `start: S`
   anywhere in the file (comments too) set the tempo and the second in the recording where `-` (beat-timed) lines begin,
   so such a file **can** be compared (a library song without times can't). The list shows the worked-out times in
   brackets; WAVs save as `<stem>-from-text.wav` (the WAV Visualizer reads that name too).

## Piano Notes Player (NOTES-TESTER/Piano-notes.html)

Made 2026-11-16: the owner wanted to see *how* a song is played. One self-contained page; it only reads files.
- **Input:** a .txt of song-library note lines only (file picker; `tempo:`/`start:` read like the Notes Tester's text option).
  The song-list drop-down was removed at the owner's request (it might confuse users). Lines are sorted by time.
  File picker look (owner's choice): blue label, deep-blue outline, deep-blue "Choose File" button with yellow text.
- **Play all notes / Play a range of bars:** two checkboxes that act as a switch. A range takes Start and End bar numbers
  (digits only, must be bars of the loaded song, start ≤ end; otherwise a red message and Play is disabled). Play then
  plays from the start bar's first line to the next bar's start and returns to the start bar; clicking the score or the
  time bar inside the range plays to the range end. Checked: bars 159–162 of Pehla Nasha play 4:28–4:35 with exactly their notes.
- **Hands** (`splitHands`): each line's notes are split into right/left groups by a cost (stay near each hand's running
  centre, each hand within an octave, first-written note in the right hand, right hand below D4 +6, left hand from F4 +4).
  Tuned on the 5-minute Pehla Nasha transcription: 975/996 lines split exactly as written (935 before tuning).
  **Fingering** (`place`): finger f rests at thumb position p + f − 1 in white-key units (left hand mirrored); the hand
  stays if the notes fit, else shifts (single note going up: thumb passes under; going down: finger 3 crosses over);
  wide chords stretch thumb to little finger. Each hand holds its notes until that hand plays again.
- **Drawing:** keyboard fitted to the song's range (at least 4 octaves, scrolls on narrow screens); hands are divs (palm +
  5 fingers, CSS transitions) over the keys, orange right / blue left, pressed fingertips go into the key (black keys higher)
  and show the finger number; pressed keys light yellow (right) / blue (left).
- **Sound:** SAMPLES/piano.js, scheduled 1.2 s ahead, the Notes Tester's soft voicing (high notes softer, chord notes
  0.55/√(n−1), 0.3 s release, low-pass 4.2 kHz, −5 dB shelf, room echo). Speed 50–115 %.
- **Score:** staff notation, built from the lines: bars from "bar N" labels (else 4 beats), each
  line a column, right hand on the treble and left hand on the bass staff, note lengths until that hand's next line;
  inside a fixed-height frame that scrolls to the current row; the current column is yellow; clicking a column plays from there.
- **Phones (≤ 576 px, added 2026-11-16 after the owner tried it on a phone):** slim one-line top bar that does not stick;
  ▶ ■ ⏱ as icons; the range row, finger numbers and sound status sit behind a ⚙️ button (`.extras`); when the whole
  keyboard can't fit at 18 px a white key, keys are drawn 18–34 px wide (sized so the two hands' usual span fits, 85th
  percentile) and `#kbdPan` slides (CSS transform) to keep both hands in the middle; the score packs ~2 bars a row
  (drawn smaller, note names bigger). Laptop layout is unchanged.
- **Falling notes view** (🎼 Staff / ⬇ Falling notes switch; phones start in falling notes): a canvas above the keys,
  3 s look-ahead, each note a bar over its key (orange right / blue left, darker for black keys), touching the keyboard
  when pressed and as long as it is held, glowing while down, with C lines and the note letter on long bars.
  `buildBars()` runs on load even when the score is hidden (the bar range needs it).
- `window.__pianoNotes` = {load(text, name), play(t), stop, showAt, lines(), songTime} for headless tests.

## Mini Piano (mini-piano.html, 2026-11-17)

Made for the owner's picture of a phone piano app showing "Pehla Nasha: F5 F5 F5 E5 F5 C6 F5 E5". One self-contained page.
- **Keys:** only C5–C6 (owner's choice: no octave buttons), 8 white keys with light-blue name tags, black keys named too.
  Tune strip above the keys (cursive title, big purple note names; the current one yellow).
- **Sound:** copied from piano.html (`ensureCtx`, soft piano bus, `NOTES-TESTER/SAMPLES/piano.js`), but only MIDI 72–84 are
  decoded; the triangle + sine synth plays until they are ready or if they are missing. The context starts on the first tap.
- **✋ Manual:** pointer events (multi-touch, slide = glissando, `touch-action:none`); a key rings while held, 0.3 s release.
  Laptop keys A W S E D F T G Y H U J K = C5…C6. **📋 Copy to table** puts the tapped keys into the table with the time
  between taps (rounded to 50 ms; last row 500 ms) and switches to Automated.
- **🤖 Automated:** table rows = key drop-down + wait (ms, whole 50–5000, else red box and Play disabled) + 🗑; ➕ Add row
  copies the last row. A row's wait = time from its key to the next key; the last row's wait is how long the last note rings;
  each note sounds for its wait (0.1–1.5 s). Starts with Pehla Nasha **bars 23–30** of the 5-min piano arrangement as piano.html plays it (owner's choice 2026-11-17;
  44.92–58.08 s, ♩ = 146, eighth = 205 ms): the 35 right-hand melody notes (all C5–C6), wait = time to the next melody note, the
  last E5 205 ms (until bar 31's F5), then three rows the owner added: F5 616, F5 205, F5 1027 (bar 23's opening again);
  38 rows, 14.98 s. Preset `ver: 4` is saved with the table; an unedited saved table with an older
  version (400 ms waits, the 25-note bars 25–31 tune, or the 35-note ver 3) is replaced. The 73 s film clip does not contain this tune; presets
  Pehla Nasha / Empty (5 rows). Tap a row's # then piano keys to fill rows in turn. ▶ Play schedules every note on
  `ctx.currentTime`; a rAF loop lights the key, the table row and the strip note. ■ Stop, Speed 50–150 %, 🔁 Loop, Space.
- **✨ Highlight keys** (checkbox next to the tune title in the strip, 2026-11-17): a guide for playing the table's tune by hand.
  The next key glows green (pulsing) and its strip note is outlined; only the right key moves it on. A run of the same key
  (F5 F5 F5) shows a green bubble above the key with the presses left (3 → 2 → 1). After the last note: "🎉 Well done!" and it
  starts again. ↺ Restart, or tap a strip note to practise from there. In Manual mode with it on, the strip shows the tune instead
  of "Your notes". Off during Automated playback and while a table row is selected for filling.
- Saved in localStorage: `miniPianoTable` (rows, name, speed, loop), `miniPianoMode`, `miniPianoGuide`.
- `window.__miniPiano` = {press, release, play, stop, setMode, rows, setRows, lit, now, playing, events, samples}.
- Checked headless (touch events at 390 px): taps play the right keys; the 25 notes light in order, at most 10–21 ms late.
- piano.html's footer was edited by hand to add the link; if piano.html is rebuilt from Piano-notes.html, keep that link.

## Music Basics Test (MUSIC-THEORY/MUSIC-BASICS-TEST-1.html, 2026-11-18)

One self-contained page; nav, step cards and pink box like the other pages.
- **Layout:** sticky score bar (Answered / Correct, ↺ Start again), a contents list grouped by Music Basics part (✅/❌ after
  submitting), one card per question, and a results box listing the topics to re-read.
- **Card:** pink box (question, "Tests:", "Topic:" link to the MUSIC-BASICS.html anchor), four options A–D (fixed order),
  a mini piano (Mini Piano look; range = smallest C-to-C span holding the question's notes, C4–C5 or C4–C6, from `rangeOf`),
  ▶ Play your option (lights the keys; ■ Stop while playing), Submit, then a result box: Correct/Wrong, what the
  wrong choice really is (`wrong[i]`), the explanation, ▶ Play the right answer, Read more, ↺ Try again.
- **Score:** the first submitted answer counts (owner's choice); retries only change the result box.
  Saved in localStorage `musicBasicsTest1` = {sel, first, last, retry}.
- **Questions:** the `QUESTIONS` array (Music Basics order). `play` strings use Music Basics' `data-play` format
  (`C4+E4+G4:2`, `r:1`) plus clicks `X x o w` (accent, beat, tick, wave), drones `~C3:4`, and `&&` for layers;
  helpers `seq`, `clk`, `bars`, `meter`, `scale`, `brokenThen`. Per-question `bpm` (default 90).
- **Sound:** Mini Piano's sample code, decoding MIDI 60–84 from `../NOTES-TESTER/SAMPLES/piano.js`, but **clearer** (the owner
  found the keys hard to tell apart with the soft voicing): low-pass 9 kHz, +2 dB treble shelf, echo 0.07, 0.1 s release.
  Band-passed noise clicks; a soft sawtooth drone for the Indian questions.
- **Shared vs different keys:** while an option plays, keys every option has light yellow and keys only some options have
  (`diffKeys`) light orange, also in the note names next to the buttons; a legend sits under the piano.
  A chord every option plays (e.g. the C major ending each Q22 example) is left out of that and stays yellow.
- **Chord questions** (Q19–Q22, Q24, Q25) play each chord note by note, then together (`brokenThen`, `then`): the owner
  found Q22's four block chords, each followed by C major, sounded the same.
- `window.__theoryTest` = {questions, parsePlay, rangeOf, check, choose, submit, play, stop, playing, lit, score, state}.
  `check()` returns problems (parsing, 4 options, a note for every wrong option, range inside C4–C6).
- Checked headless (2026-11-18): `check()` empty; 11 answers worked out from their notes agree with the key; every topic
  anchor exists; first-answer scoring, retry and reload; keys light in order; 390 px page has no sideways scroll.

## How new songs are made (from 2026-11-17)

The owner supplies **sheet music as a PDF** (e.g. `S-PAD/PEHLA-NASHA-notes.pdf`, `S-PAD/fur-elise-beethoven-notes.pdf`;
`S-PAD/` is git-ignored). Claude Code reads it into a `.txt` of song-library.js note lines in `REFERENCE-AUDIO-FILES/`
(bar labels, tempo, both hands; see the two sections below for how), which the Piano Notes Player / piano.html play.
The old method (notes found by WAV analysis plus web searches, kept in `MUSIC-NOTES/*.html` sheet pages) is retired:
that folder was moved to `S-PAD/MUSIC-NOTES/` on 2026-11-17 and the Notes Tester's "sheet music" option was removed.

## Für Elise from a vector PDF (2026-11-16)

`REFERENCE-AUDIO-FILES/SONG-6-FUL-ELISE-BEETHOVEN.txt` (owner's file name) was made **fully by code** from
`S-PAD/fur-elise-beethoven-notes.pdf`, a MuseScore 3.6 export (public-domain piece). Unlike the Pehla Nasha screenshots, a
MuseScore PDF stores every symbol as a SMuFL music-font character (Leland: E0A4 note head, E4E3–E4E7 rests, E240–E243
flags, E1E7 dot, E260–E262 flat/natural/sharp, E050/E062 clefs, E044 repeat dots, E510 8va) at exact coordinates, and
staff lines, stems, bar lines and beams as vector paths. Reader (scratchpad `vecomr.py` / `vecomr2.py` / `fe_gen.py`,
PyMuPDF): staves from 5-line paths; bar lines = 0.89/2.73 pt verticals over the treble staff; stems = 0.55 pt verticals
at a head's left/right edge; beams counted where the quad actually meets the stem; cross-staff beam groups timed with
the staff most of their notes are on; per-staff columns timed by "next column starts when the earliest sounding event
ends"; triplets from the italic "3" (and implied when a bar of beamed notes is 3/2 too long); accidentals carried
through the bar; ties from short flat curves (also across system breaks); 8va up to its hook; 1st/2nd endings and
repeats written out (106 printed measures → 127 played). Every bar checks to 3/8 (pickup 1/16 × 2 + 1st ending
complete each other). No tempo in the score ("Poco moto"): ♩ = 70, start 0.5 s, 778 lines, 2:42. Grace notes skipped.

## Pehla Nasha solo piano arrangement (2026-11-16)

The owner chose the MuseScore solo piano arrangement by Nakul Jogdeo (musescore.com/user/38705085/scores/11781643;
MuseScore blocks fetching, so the owner saved screenshots of it as `S-PAD/PEHLA-NASHA-notes.pdf`). All 177 bars, both
hands, were read from those images: a note-head template matcher (staff lines, barlines, head pitch) plus checking each
bar by eye; every bar adds up to 4 beats. Grace notes, trills and rolls are left out. 4/4, F major; tempo ♩ = 112 (bar 1),
121 (bar 11), 133 (bar 19), 146 (bar 23 to the end), about 5:00. Many bars repeat (39–48 = 99–108 ≈ 159–168, etc.).
- `REFERENCE-AUDIO-FILES/SONG-3-PEHLA-NASHA-ORGIG-NOTES-5MIN.txt` (owner's file name, "ORGIG" kept): 996 song-library
  lines with seconds from the tempo marks, bar 1 at 0.41 s; right hand first (melody = main note), then the left hand.
- The same notes were also put in a sheet-music page, now retired in `S-PAD/MUSIC-NOTES/SONG-3-pehla-nasha-notes.html`.
- Only bar 1 matches the 73 s film clip (`SONG-3-pehla-nasha-start.wav`); Compare against it flags almost everything
  after that. Comparing properly needs a recording of this arrangement.
2. **Test notes:** renders every note line with an `OfflineAudioContext`, using copies of the practice page's
   `tone()` / `ksBuffer()` voices (Karplus-Strong noise is seeded, so the output is identical every time). Each note
   starts at its written time and the render is as long as the original, so times line up. It renders in 4 s chunks
   (only the notes sounding in each); one context with every note connected was 10× slower. Mixing is linear, then
   `tanh` soft clip and normalise. "Match the recording's tuning" shifts the synth by the measured cents.
   **Real instrument sound** (ticked by default; the owner found the oscillator voices sounded "like MIDI"): each
   note plays a recorded sample from `NOTES-TESTER/SAMPLES/<piano|guitar|accordion>.js` (FluidR3_GM SoundFont,
   CC BY 3.0, via gleitz/midi-js-soundfonts; grand piano, steel-string guitar, accordion; one base64 MP3 per MIDI
   note 33–96, 1.5–2.2 MB each). The file is added as a `<script>` only when needed, so it works on `file://`.
   Each sample is decoded once, its MP3 lead-in silence is cut (keeps onsets on time) and its peak set to 0.6;
   pitch shifts (tuning, slides) use the source's `detune` / `playbackRate`.
   **Softer piano (2026-11-16; the owner said it sounded "like a spoon on a steel bowl" once chords were added):** piano
   notes above D5 get quieter (down to 0.5×), chord notes other than the first-written one play at 0.55/√(n−1), chords
   roll 12 ms per note (not 30), release is 0.3 s like a sustain pedal, and the piano bus goes through `pianoRoom()`
   (low-pass 4.2 kHz, −5 dB high shelf at 2.2 kHz, seeded 1.6 s convolution echo at 0.22). The mix is scaled so its
   99.9th percentile is 0.6 before `tanh`: a plain `tanh` on the raw mix was distorting loud chords.
   Controls after the change: Pehla Nasha 246/246, Tip Tip 93/93, the 996-line text file 979/996.
   **🎛️ Controls box** (yellow, under the Test/Stop/Download buttons; the owner asked for synthesizer-style controls):
   `TONE_SLIDERS` = brightness (low-pass 1–12 kHz, 12 = off), treble (high shelf), warmth (low shelf 250 Hz), soften
   high notes, chord/left-hand level, attack, sustain (release), room echo, room size; presets (`TONE_PRESETS`: soft
   default, very soft, bright, warm, concert hall, dry) and ↺ Reset. Values are in `TONE`, saved in localStorage
   (`notesTesterTone`), and part of the render cache key, so a change re-renders on the next Test / Compare / Download.
   They shape the piano only (a note says so for guitar/accordion songs). A long room size slows rendering (hall ≈ 3×). A note with no sample, or a failed
   load, falls back to the `tone()` synth voice. Unticking the box gives the old synth.
   **Add a soft band** (`#bandBox`, off by default; the owner wanted it to sound fuller): bass + chords **measured
   from the recording** (`measureChords`): per beat (song tempo), salience C2–B5 folded to 12 pitch classes (below
   G3 ×1.5, written melody notes ×0.5), cosine match against 24 major/minor triads, +0.06 for chords of the key
   (`keyInfo` parses `key`), +0.05 when the bass is the root, a no-chord state for near-silence, then Viterbi with a
   0.12 change penalty. `bandEvents`: root bass on even beats, triad (F3–E4) on odd beats, strummed on guitar,
   shorter on accordion, on its own bus at 0.17 (melody 0.5). The chords found are listed in `#bandInfo`. It needs
   the recording, so on `file://` press Compare once first. Compare's control always renders the melody alone.
   **⬇ Download WAV:** 16-bit, **stereo**, 48 kHz (same as the recordings), named `<audio>-from-notes.wav`
   (`-from-text` for a text file, `-band` with the band, `-tuned` with the tuning box; the same name is overwritten).
   Entries that share a recording get their own name: the entry's `wavTag` goes after `-from-notes`
   (e.g. `…-from-notes-v2.wav`; no entry uses one since the Pehla Nasha draft was merged); a later entry without one gets `entryN`. The WAV Visualizer
   reads the tag back to choose that entry's note lines and to list only its files in TEST-FILES. It saves into
   **`NOTES-TESTER/TEST-FILES/`** (the owner's choice): the first click asks for the folder (`showDirectoryPicker`),
   the handle is kept in IndexedDB (`notes-tester` / `saveDir`), later clicks write straight into it. A
   "Change folder" link re-picks it. Browsers without the API fall back to a normal download.
3. **Compare audio files:** a musical comparison, not a waveform diff (a synth never matches a recording sample for sample).
   The DSP is a JS port of `SCRIPTS/musicdsp.py`: mono 22 050 Hz, STFT 4096/8192 hop 256, tuning (circular mean),
   harmonic salience (6 harmonics), spectral-flux onsets. Two real frames share one complex FFT (`frameMag2`).
   - Per line: `OK` (a written note in the 3 strongest **and** an onset within ±80 ms), `PITCH?`, `OCTAVE?` (best
     shape-preserving shift is ±12), `TIME?` (onset 80–250 ms away), `EXTRA?` (no onset and no pitch).
     `MISSING` = a strong unlisted onset; re-strikes of the sounding note (or its octave) are only counted.
   - The same analysis runs on the synth as a **control**; if it reads back < 90 %, the report warns.
   - The report lists **every** line (owner's choice), with a suggested replacement line in song-library.js format,
     then "Lines to fix". Thresholds are in `CFG` at the top of the script.
   - On `file://` the page can't fetch the WAV, so it shows a single-file picker for the original.
- Results on the current library (2026-11-15; Pehla Nasha's notes were replaced on 2026-11-16): Inteha 62/68 OK, Tip Tip 93/93, Pehla Nasha 185/186, Chura 81/82,
  Anhoni 118/141 (after the 2026-11-15 fixes: 151/151). Measured tunings match the Python scripts within 1 cent.
- The owner's PC (Pentium Silver N5030) is slow, more so when Folding@home is running: Compare takes ~3–12 s there.
- `window.__notesTester` exposes `compare`, `testNotes`, `report`, `synth`, `wavBlob` for headless tests.

## WAV Visualizer (NOTES-TESTER/WAV-VISUALIZER.html)

One self-contained page, same look as the Notes Tester. It only reads files.

1. **Choose the two WAVs:** the left box takes the original and the right box the Notes Tester's file, each with a file picker.
   The optional song drop-down gives the written note lines, and over http(s) it also fetches the original. A file name is
   matched to its song by its stem (`-from-notes…` removed). **📁 Look in TEST-FILES** uses the Notes Tester's saved folder handle
   (IndexedDB `notes-tester` / `saveDir`) to list `<stem>-from-*.wav`. A warning appears if the stems differ or the lengths differ by more than 0.5 s.
   Per the owner, the Notes Tester link is a **plain link**, with no `?song=` parameter.
2. **▶ Analyse:** the Notes Tester's DSP is copied into the page. The original's tuning is used for both files. Salience of C1–C7 in
   every frame is computed once in two flavours: S6 (6 harmonics, as the tester) and S4 (4 harmonics, as `track_melody.py`).
   Changing a setting only rebuilds the boxes:
   - **All notes** (the default): per frame, up to N (default 3) local peaks ≥ threshold × the frame's strongest note. A note
     12, 19 or 24 semitones **below** a stronger one is dropped unless it is ≥ 0.9 × as strong (sub-octave ghost); **above** a stronger
     one, it is kept when it is ≥ 0.5 × as strong (`GHOST_UP`). The earlier rule (0.9 both ways) hid the Pehla Nasha tune wherever the band doubled it an octave lower.
     Notes are joined over gaps < 30 ms, split at an onset when the note gets louder, kept when ≥ 50 ms, and their starts are
     snapped to an onset within 0.1 s.
   - **Melody only:** the `track_melody.py` Viterbi. It works best with a narrowed pitch range.
3. **Boxes:** one canvas per file, rows = semitones, colour = **note name + octave** (one hue per name, lighter higher up; the owner's choice).
   Opacity shows strength. A **red** outline = the box is only in this file. **Orange** = the other file has the note an octave away
   ("Ignore octave", on by default). Two boxes match when they have the same note and their starts are within 80 ms or they overlap
   by half. **Written note lines** are drawn dashed with `#N` (on by default). Phone: the boxes stack. Zoom and scroll are shared:
   drag, Shift/Ctrl + wheel, pinch, − + ⟲, and a minimap. Clicking a box plays that slice of that file, then the note (`tone()`
   without samples). Playback uses `<audio>` elements with `preservesPitch`: Original, Generated, or Both (panned L/R), with speed,
   loop of the visible part and Space.
4. **📋 Copy differences:** with a song chosen, the report is **line-based** (a list of every box was ~500 rows of band notes):
   A = the written lines none of whose notes is among the 3 strongest (`TOP_N`) of the lines' range, averaged 0.03–0.18 s after the
   line (the Notes Tester's pitch check, read from the stored salience; boxes missed quiet solo notes: 37 false alarms on the flute draft);
   B = original-only notes of strength ≥ 0.5 with no line near them. Both only look at the lines' pitch range ±2 semitones.
   It says how many lines each file plays, and warns when the generated file plays < 90 % (a stale file or the wrong entry).
   A generated file's `wavTag` (see the Notes Tester) picks its library entry automatically.
   With no song chosen, it lists every unmatched box with strength ≥ 0.25.
- Checks (2026-11-16): the same file on both sides is 100 % matched. Against the original Pehla Nasha entry's lines, the
  generated file plays 186/189 and the original 179/189 (137/189 before the `GHOST_UP` change).
  Analyse takes ~16 s for two 73 s files.
- `window.__wavViz` exposes `analyse`, `loadFile`, `F`, `view`, `CFG`, `lines()`, `results`, `report()`, `setSong(i)` for headless tests.

## Piano Capture (NOTES-TESTER/Piano-tester.html, renamed from Piano.html by the owner)

Made 2026-11-16 because the owner found the Pehla Nasha timing still off. One self-contained page; it only reads files.
- **Piano:** 88 keys (A0–C8), drawn as absolutely placed divs, scrolls sideways. Sound = `SAMPLES/piano.js` (decoded at load,
  lead-in trimmed, held while the key is down), triangle + sine synth outside MIDI 33–96.
- **⌨️ Manual mode:** laptop keys by `e.code` (any layout): bottom row Z S X D C V G B H N J M , L . ; / from `baseC` (default
  C4), top row Q 2 W 3 E R 5 T 6 Y 7 U I 9 O 0 P [ = ] an octave up; ←/→ shift an octave; mouse/touch on the keys too.
  **● Record** (or Space): with "Play the WAV while I record" the WAV plays (start time, speed 50–100 % with preservesPitch,
  volume) and every key down/up is stamped with **`audio.currentTime`**, so times are seconds in the WAV even when slowed down.
  Without a WAV, times count from ● Record. "Add to the lines already in the box" records a song in parts.
- **Two hands (2026-11-16, the owner saw a two-hand piano cover; the right hand stays the flute melody):** 📥 Start from the
  song's lines puts the song-library lines in the box (and ticks "Add"). An add pass keeps every existing line as it is
  (time, beats, main note first, `~`/`^`/`@`/label) and appends each new chord group's notes to the nearest existing line
  within **"Join a stroke to a line within"** (default 0.12 s); strokes further away become new lines. Needed because the
  Notes Tester plays a line only until the next line starts, so two hands as separate lines 0.02 s apart would cut each other off.
  Limit: a left-hand chord can't be held under several melody notes (the format has one note list; that would need a
  separate left-hand part in song-library.js).
- **🎧 WAV mode:** "Find the notes" runs the WAV Visualizer's DSP (copied in) on the whole file: Melody (track_melody Viterbi,
  default C4–C7, strength ≥ 0.1) or All notes; ▶ Play then lights the keys from the found notes (optionally sounding them).
  On Pehla Nasha it reproduces 244/246 of the current lines within 80 ms (they came from the same tracker), so the
  hand-played mode is the one that adds new timing information.
- **Output box:** song-library.js lines `'time  notes  beats',` with a `// Piano.html <date>: <source>; tempo` header;
  key strokes within 0.05 s form a chord line (highest note first); beats = held seconds × tempo / 60, rounded to ¼
  (tempo from the chosen song, editable). The box is editable; 📋 Copy. `window.__piano` exposes press/release/startRec/
  stopRec/analyse/loadWav/events/out/setMode for headless tests.

## Working on it

- **Testing:** open `index.html` straight from disk or through GitHub Pages; both work.
  - For automated checks, headless Chrome with a Node CDP script (`--remote-debugging-port`, `--autoplay-policy=no-user-gesture-required`, `--mute-audio`) can play the audio in real time.
  - Use it to check the highlight moves forward through all notes, and take screenshots at 390 px (phone) and 1280 px (laptop) widths.
  - `--dump-dom` with virtual time does **not** play media.
- **Git:**
  - Git Bash on Windows.
  - Commit messages end with a `Co-Authored-By` line.
  - **Ask before pushing.** The owner normally confirms each push with "yes push it".
  - Pushing to `main` deploys the live site within a minute or two.
- **Recordings:** the owner chose to commit the WAV files to this public repo. (In the BLOG repo, `audio/` stays git-ignored.)
- **Recording tool:** `C:\Daya\RAGchamp\BLOG\AUDIO-RECORDER.py` (PyAudioWPatch WASAPI loopback) records whatever is playing on the PC into WAV files.
  It's handy for capturing new reference clips.

## Pehla Nasha flute melody (2026-11-15, adopted 2026-11-16)

The owner listened to the Pehla Nasha notes: only lines 27–97 (17.1–44.0 s) sounded like the recording; the
tune is played on a **flute** (instrumental, no singing in 0–17 s and 44–73 s). The first analysis kept notes
C4–A5 only, so it missed the flute's **C6** notes in the intro. No free published notes cover the instrumental
parts (notesandsargam.com has the sung tune only). `SCRIPTS/track_melody.py` (lead-line Viterbi, C4–C7,
4 harmonics, octave penalty 0.2, jump cost 0.2; tuned to agree with 72/73 of the trusted lines) made the entry
**"Pehla Nasha: opening, flute draft (check by ear)"** in song-library.js: tracker notes for 0–17.1 s and 44.1–73 s,
the original lines 27–97 in between. On 2026-11-16 the owner chose it: its 246 lines (tempo 78) replaced the
"Pehla Nasha: opening" notes and the draft entry was deleted, so each song now has one entry again. The two entries had
been mixed up: the practice page showed the draft while the Notes Tester showed the old entry (same title start, same recording).
