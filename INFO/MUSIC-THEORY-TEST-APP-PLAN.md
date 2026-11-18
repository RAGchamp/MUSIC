# Music Basics Test 1: plan

**Status:** approved and built (2026-11-18): `MUSIC-THEORY/MUSIC-BASICS-TEST-1.html`. The owner chose the recommended
answer to every question in section 10. Built as planned, except:
- The questions follow the Music Basics order (owner's choice), so the numbers differ from the table in section 4:
  Q1 notes, Q2–Q5 Indian music (Pa, tivra Ma, Bhupali, Teentaal), Q6–Q25 Part D (13.2 durations … 20.1 Neapolitan).
- **▶ Play your option** turns into **■ Stop** while it plays (instead of restarting).
- After Submit each option gets a small **▶ hear** button, so all four can be compared.
- A **beat light** (red = bar/sam, orange = beat/clap, yellow = tick, light blue = wave) flashes for the rhythm questions.
- "↺ Try this question again" shows only while the latest answer is wrong.

## 1. Goal

A new page, `MUSIC-THEORY/MUSIC-BASICS-TEST-1.html` (live at
https://ragchamp.github.io/MUSIC/MUSIC-THEORY/MUSIC-BASICS-TEST-1.html), that tests what a student has learnt from
`MUSIC-THEORY/MUSIC-BASICS.html`. It is a multiple-choice quiz where **every answer can be heard and seen on a piano**:
the student doesn't just pick a word, they play their choice, hear why it is right or wrong, and see the keys light up.
The aim is that the student grasps each basic idea *and* hears how it is applied.

"TEST-1" leaves room for later tests (TEST-2, …) built the same way with other questions.

## 2. Page layout (top to bottom)

1. **Top nav**, the same as MUSIC-BASICS.html (deep blue `#04264d`, yellow `#ffd60a`, `../logo.svg`, tagline
   "Music Practice App"); slim, one line and not sticky on phones, like mini-piano.html.
2. **Title and intro:** "Music Basics: Test 1", one line on how it works ("Pick an answer, press ▶ Play your option to
   hear it, then Submit"), and a link back to Music Basics.
3. **Score bar** (sticky under the title on laptop, plain on phones): `Answered 7 / 25 · Correct 6` and **↺ Start again**.
4. **Table of contents:** every question as a numbered link (`Q1. How many notes in an octave?`), grouped by the part of
   Music Basics it tests (Part A Western basics, Part B Indian music, Part D theory groups). After a question is submitted
   its line gets ✅ or ❌, so the contents doubles as a progress list.
5. **One card per question** (section 3), each with an anchor `#q1`, `#q2`, … and "↑ Back to contents" at the bottom.
6. **Results box** at the end: score, and a list of the questions answered wrongly with links to the questions and to
   the Music Basics topics to re-read.
7. **Footer** like MUSIC-BASICS.html, with links to Music Basics, the Mini Piano and the main app.

Bootstrap 5.3.3 from the jsDelivr CDN, everything else inline in the one file; no build step. Works opened from disk
and on GitHub Pages. Phone (390 px) and laptop (1280 px) layouts both checked.

## 3. One question card

```
┌─ Q5 ───────────────────────────────────────────────────────────┐
│ ┌─ pink box ─────────────────────────────────────────────────┐ │
│ │ Which pair of notes is a WHOLE step apart?                 │ │
│ │ Tests: half steps vs whole steps                           │ │
│ │ Topic: 13.6 Steps and Accidentals  → (link)                │ │
│ └────────────────────────────────────────────────────────────┘ │
│  ○ A  E4 – F4                                                  │
│  ○ B  B4 – C5                                                  │
│  ● C  C4 – D4                                                  │
│  ○ D  F4 – F#4                                                 │
│                                                                │
│  [ mini piano: big keys with name tags, C4 … C5 ]              │
│                                                                │
│  [ ▶ Play your option ]   [ Submit ]                           │
│ ┌─ result box (after Submit) ────────────────────────────────┐ │
│ │ ✅ Correct!  /  ❌ Wrong: the answer is C                   │ │
│ │ Explanation (2–4 sentences) + [▶ Play the right answer]    │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

- **Pink box** (the app's `.about-box` style: pink background, rounded): the question in bold, a "Tests:" line saying what
  idea it checks, and a "Topic:" line with the section number and name, linked to its anchor in MUSIC-BASICS.html
  (e.g. `MUSIC-BASICS.html#t-steps`, opens in the same tab; the student can come back with Back).
- **Four options** (A–D) as big radio rows (easy to tap on a phone). The order is fixed (not shuffled) so the answer key
  in the code stays simple; the correct letter varies from question to question.
- **Mini piano** below the options, drawn like mini-piano.html: white keys with rounded bottoms and light-blue name tags,
  named black keys, a pressed key turns yellow `#ffc107` and dips. The student can also tap the keys freely to try
  things out (multi-touch pointer events, the key rings while held). Range: see section 5.
- **▶ Play your option** is disabled until an option is chosen. It plays the chosen option's example on the piano and
  lights the keys as they sound (chords light together). Pressing it again while playing stops and restarts. Choosing
  another option stops any playing example.
- **Submit** is disabled until an option is chosen. After Submit the options lock, the right option turns green, a wrong
  choice turns red, and the **result box** appears:
  - **Correct** (green border) or **Wrong** (red border) with the right letter;
  - an **explanation**: why the right answer is right and, where it helps, what the student's wrong choice actually was
    (e.g. "B4 – C5 is only a half step: there is no black key between B and C");
  - **▶ Play the right answer**, so the student hears the difference (they can still play any option after submitting);
  - "Read more: 13.6 Steps and Accidentals" link.
- **Try again:** a small "↺ Try this question again" link in the result box unlocks just that question (the score keeps
  the first answer; see section 10, Q4).

## 4. Questions (draft: 25)

Every option has an example that can be played, so "Play your option" always does something useful. Notes are written
the song-library way (`C4`, `F#4`, `Bb4`); a "C" chord means C4+E4+G4 unless stated. All examples fit in C4–C6.

| # | Question | Tests | Topic (anchor) | Options (✔ = right) | What each option plays |
|---|---|---|---|---|---|
| 1 | How many different notes (white and black keys) are there in one octave before the names repeat? | the 12 notes | 1 (`#notes`) | A 7 · B 8 · **C 12 ✔** · D 10 | 7 white keys C–B; C4–C5 (8 keys, the last is C again); all 12 C4–B4; 10 notes C4–A4 chromatic |
| 2 | Which pair of notes is a **whole step** apart? | half / whole steps | 13.6 (`#t-steps`) | A E4–F4 · B B4–C5 · **C C4–D4 ✔** · D F4–F#4 | the two notes, one after the other, then together |
| 3 | Which note lasts **2 beats** in 4/4? | note durations | 13.2 (`#t-duration`) | A whole · **B half ✔** · C quarter · D eighth | C5 held 4 / 2 / 1 / ½ beats over a soft 4-beat click |
| 4 | How many beats does a **dotted half note** last? | dots | 13.5 (`#t-dots`) | A 2 · **B 3 ✔** · C 4 · D 1½ | C5 held that many beats over the click |
| 5 | Which bar is **complete** in 3/4? | measures and time signatures | 13.3 (`#t-measures`) | **A half + quarter ✔** · B half + half · C quarter + quarter · D whole | the rhythm on C5 over a 3-beat click (wrong ones run over or stop short) |
| 6 | Which rest is silent for a whole 4/4 bar? | rests | 13.4 (`#t-rests`) | A quarter rest · B half rest · **C whole rest ✔** · D eighth rest | C5, the rest's silence over the click, C5 again |
| 7 | Which time signature is **compound duple** (2 beats, each split into 3)? | simple vs compound meter | 14.1 (`#t-simple`) | A 3/4 · **B 6/8 ✔** · C 2/4 · D 4/4 | two bars of eighth-note clicks with that meter's accents |
| 8 | Which is an **odd meter**? | odd meter | 14.2 (`#t-odd`) | A 6/8 · B 4/4 · **C 7/8 ✔** · D 2/2 | accented clicks: 7/8 as 2+2+3 |
| 9 | Which step pattern builds a **major scale**? | the major scale | 15.1 (`#t-major`) | **A W W H W W W H ✔** · B W H W W H W W · C W W W H W W H · D H W W W H W W | each pattern played up from C4 (major, natural minor, Lydian, Locrian-like) |
| 10 | Which is **A harmonic minor**? | the three minor scales | 15.2 (`#t-minor`) | A A B C D E F G A · **B A B C D E F G# A ✔** · C A B C D E F# G# A · D A B C# D E F# G# A | each scale from A4 to A5 |
| 11 | In C major, which note is the **dominant** (5th degree)? | scale degrees | 15.3 (`#t-degrees`) | A F · B B · **C G ✔** · D E | C major scale up to the chosen note, which is held |
| 12 | Which major key has **two sharps** (F# and C#)? | key signatures | 15.4 (`#t-keysig`) | A G · **B D ✔** · C A · D Bb | that major scale |
| 13 | **C4 to E4** is a… | interval quality | 16.2 (`#t-specific`) | **A major 3rd ✔** · B minor 3rd · C perfect 4th · D major 2nd | the interval named, from C4 (C–E, C–Eb, C–F, C–D) |
| 14 | A **major 3rd** turned upside down becomes a… | interval inversion | 16.4 (`#t-inversion`) | A major 6th · **B minor 6th ✔** · C minor 3rd · D perfect 5th | C4–E4, then the named interval E4 up (E–C, E–C#, E–G, E–B) |
| 15 | Which triad is **C minor**? | the four triad types | 17.1 (`#t-triads`) | A C E G · **B C Eb G ✔** · C C Eb Gb · D C E G# | the chord, broken then together |
| 16 | Which voicing is **C major in second inversion**? | triad inversion | 17.2 (`#t-triadinv`) | A C4 E4 G4 · B E4 G4 C5 · **C G4 C5 E5 ✔** · D G4 B4 D5 | the chord, lowest note first |
| 17 | Which chord is **G7** (dominant seventh)? | seventh chords | 17.3 (`#t-sevenths`) | **A G B D F ✔** · B G B D F# · C G Bb D F · D G Bb Db F | the chord (G4 up) |
| 18 | In C major, which chord is **ii**? | Roman numerals | 18.2 (`#t-rn3`) | A D F# A · **B D F A ✔** · C F A C · D E G B | the chord, then C major I so the student hears it in the key |
| 19 | Which progression is a **perfect (authentic) cadence** in C? | cadences | 19.2 (`#t-cadences`) | A F → C · B C → G · **C G → C ✔** · D G → Am | the two chords (plagal, half, authentic, deceptive) |
| 20 | Over a C chord the melody goes **C – D – E**. What is the D? | nonharmonic tones | 19.1 (`#t-nht`) | **A passing tone ✔** · B neighbour tone · C suspension · D appoggiatura | each kind over a held C chord (C–D–E; E–F–E; held D resolving to C; leap to D resolving to E) |
| 21 | In **C minor**, which chord is the **Neapolitan sixth**? | building the Neapolitan | 20.1 (`#t-neabuild`) | **A F4 Ab4 Db5 ✔** · B F4 A4 D5 · C Eb4 G4 C5 · D F4 Ab4 D5 | the chord, then G7 → Cm so it is heard in use |
| 22 | If **Sa = C**, which note is **Pa**? | the seven swaras | 5.1 (`#swaras`) | A F · **B G ✔** · C A · D E | Sa (C4), then the note, with a soft drone on C |
| 23 | If **Sa = C**, which note is **tivra Ma**? | komal and tivra swaras | 5.2 (`#swaras`) | A F · **B F# ✔** · C E · D Db | Sa, then the note, over the drone |
| 24 | Which notes does **Raga Bhupali** use (Sa = C)? | ragas | 6 (`#raga`) | A C D E F G A B · **B C D E G A ✔** · C C D Eb F G Ab Bb · D C D F G A | the notes going up and back down (aaroh, avroh) |
| 25 | How many beats (matras) are in one cycle of **Teentaal**? | tala | 7 (`#tala`) | A 8 · B 6 · **C 16 ✔** · D 7 | one cycle of clicks with sam accented (Keherwa, Dadra, Teentaal, Rupak) |


The explanations are written from the Music Basics text itself, so the words match what the student read (e.g. Q25:
"Teentaal is 16 beats, 4 × 4. Clap on 1, 5 and 13 and wave on 9 (khali). 8 is Keherwa, 6 is Dadra, 7 is Rupak.").

## 5. Mini piano on each card

- Drawn by one function `buildPiano(el, low, high)` taken from mini-piano.html (same CSS, keys absolutely placed so black
  keys sit between white ones), one per question card.
- **Range per question:** each question gives the smallest C-to-C range that holds all four options' notes, at least one
  octave: most use **C4–C5** (8 white keys, as big as the Mini Piano's), some **C4–C6** (15 white keys, ~24 px each on a
  390 px phone, which is still tappable). This keeps the keys big wherever possible.
- Free play: pointer events (multi-touch, slide = glissando), a key rings while held, 0.3 s release, exactly as in the
  Mini Piano. No laptop-key mapping (25 pianos on one page would fight over the keyboard).

## 6. Sound

- Copied from mini-piano.html: `ensureCtx()` (soft piano bus: low-pass 4.2 kHz, −5 dB shelf, small room echo,
  compressor) and the sample loader for `../NOTES-TESTER/SAMPLES/piano.js` (FluidR3_GM, CC BY 3.0), decoding
  **MIDI 60–84** (C4–C6, 25 notes). The triangle + sine synth plays until the samples are ready or if they are missing.
  The audio context starts on the first tap (browsers need a gesture).
- **Rhythm click** for the meter, duration and tala questions: a short synthesised wood-block click (filtered noise
  burst); accented beats louder and higher.
- **Drone** for the Indian questions: a soft sustained Sa + Pa (C3 + G3) under the example, like Music Basics' tanpura
  button.
- **One sound at a time on the page:** starting any example stops whatever else is playing.

### Example format

Each option's example is a token string in the same format as Music Basics' `data-play` buttons, so it is easy to write
and check: `C4:1 C4+E4+G4:2 r:1` (note or chord : beats, `r` = rest), plus three extras for this page:
`x` = click, `X` = accented click, and a per-question `drone: true`. Example: Q3 option B =
`C5:2 r:2` with `click: 4` (four clicks under it). Tempo per question (default ♩ = 90). `playTokens()` schedules every
note on `ctx.currentTime` and a rAF loop lights the keys at the right moments.

## 7. Data and code

All questions live in one array at the top of the script, so new tests can copy the page and change only this:

```js
const QUESTIONS = [
  { id: 2, group: 'Part D · The Basics',
    q: 'Which pair of notes is a whole step apart?',
    tests: 'Half steps vs whole steps',
    ref: { href: 'MUSIC-BASICS.html#t-steps', label: '13.6 Steps and Accidentals' },
    range: ['C4', 'C5'], bpm: 90,
    options: [
      { text: 'E4 – F4',  play: 'E4:1 F4:1 E4+F4:2' },
      { text: 'B4 – C5',  play: 'B4:1 C5:1 B4+C5:2' },
      { text: 'C4 – D4',  play: 'C4:1 D4:1 C4+D4:2' },
      { text: 'F4 – F#4', play: 'F4:1 F#4:1 F4+F#4:2' },
    ],
    answer: 2,                       // index into options (C)
    explain: 'A whole step is two half steps: C to D skips the black key C#. E–F and B–C have no black key between them, so they are half steps; F–F# is also a half step.',
    wrong: { 0: 'E–F is a half step: there is no black key between E and F.' }   // optional, per wrong option
  },
  // …
];
```

- **Saved progress:** `localStorage` key `musicBasicsTest1` = `{ answers: {qid: optionIndex}, firstTry: {qid: optionIndex} }`
  (in try/catch; the page works without it). Reloading shows submitted questions as submitted. ↺ Start again clears it.
- `window.__theoryTest` = `{ choose(q, i), submit(q), play(q, i), stop(), score(), questions }` for headless tests.

## 8. Checks before it is called done

- A headless Chrome script (as for the other pages) answers every question right and wrong: score, ✅/❌ in the
  contents, result box text and colours.
- Every option's `play` string parses, every note is inside that question's piano range, and every example plays and
  lights the keys in order (no key lit that the string doesn't contain).
- An automatic check of the answer key: for interval, chord, scale and key questions the script works out the right
  answer from the notes (e.g. counts semitones) and compares it with `answer`, so a typo in the key is caught.
- Every `ref.href` anchor exists in MUSIC-BASICS.html.
- Screenshots at 390 px and 1280 px.

## 9. Other changes

- MUSIC-BASICS.html: a "📝 Test yourself: Music Basics Test 1" link at the end of Part D (Key Takeaways, section 12) and in
  the footer.
- The site map page and contactus.html cards: add the test.
- CLAUDE.md: a row in the Files table and a short "Music Basics Test" section.
- Commit; ask before pushing.

## 10. Owner's decisions (2026-11-18)

1. **Number of questions:** keep all 25.
2. **Piano range:** per question: C4–C5 where the answers fit, C4–C6 only when needed.
3. **Order:** the Music Basics order (Part A, Part B, Part D).
4. **Retries:** allowed; the score counts the first answer only.
5. **Options:** fixed order, not shuffled.
6. **View:** one long page with the table of contents (no one-at-a-time view).
