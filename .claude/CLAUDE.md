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
| `logo.svg` | The logo in the top nav (a copy of the BLOG logo). |
| `REFERENCE-AUDIO-FILES/song-library.js` | **The song list.** It defines `window.SONG_LIBRARY`, which fills the song drop-down. |
| `REFERENCE-AUDIO-FILES/*.wav` | Song recordings, e.g. `SONG-1-inteha-ho-gayi-start.wav` (22 s, 4 MB). |
| `REFERENCE-AUDIO-FILES/SONG-1-inteha-ho-gayi-notes.txt` | Old analysis notes. Its times come from an **earlier** recording and **do not** match the current WAV. The app doesn't use it. |
| `readme` | The original one-line readme from GitHub. |

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
    inst:  'guitar',                             // what the recording is played on; only a hint
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
3. Commit and push.

A song with no `audio` can't be played: the Play button is disabled.

The Inteha timings (68 notes) came from pitch and onset analysis of the clip with numpy/scipy:
STFT, a double-stop salience score, spectral-flux onsets, and a tuning offset of about −10 cents.
They were then cleaned up by hand against the owner's tab.

## How the page works (index.html)

1. **Choose a song:** `#songSel` lists `library`. Choosing one shows the key, the note count and the file name in `#songMeta`.
2. **Instrument:** two **checkboxes**, `#instPiano` and `#instGuitar`, that act as a pair: ticking one unticks the other.
   The owner asked for checkboxes, so keep them; don't switch to radio buttons.
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
- guitar is a Karplus-Strong plucked string (`ksBuffer`) through a small body EQ.

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
