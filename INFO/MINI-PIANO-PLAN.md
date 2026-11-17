# Mini Piano: plan

**Status:** approved and built (2026-11-17): `mini-piano.html`. Open questions answered (section 9).
Built as planned, except: "tap a row's # then tap piano keys" fills rows in turn (instead of filling the row whose
drop-down has focus: a phone's drop-down picker hides the keys); on a sideways phone the top bar and strip are made smaller.

## 1. Goal

A new page, `mini-piano.html` in the site root (`C:\Daya\RAGchamp\MUSIC\mini-piano.html`, live at
https://ragchamp.github.io/MUSIC/mini-piano.html), made for **phones**. It shows a small piano like the
"Pehla Nasha" picture the owner shared: one octave of big keys, **C5 to C6** (8 white keys, 5 black keys), with the
note name printed on each white key (C5, D5, E5, F5, G5, A5, B5, C6). Users practise short tunes on it, such as
`F5 F5 F5 E5 F5 C6 F5 E5` (the opening of Pehla Nasha shown in the picture).

It has two modes, chosen with a switch at the top:

1. **✋ Manual:** the user taps the keys and hears them.
2. **🤖 Automated:** the user fills a table of keys and wait times and presses **▶ Play**; the page presses the keys
   by itself (they light up) and plays them.

## 2. Look (from the picture)

- Same top nav as the other pages (deep blue `#04264d`, yellow `#ffd60a`, `logo.svg`, tagline "Music Practice App"),
  but slim on phones like `piano.html` (one line, not sticky).
- Title **Mini Piano** and a one-line hint ("Tap the keys, or fill the table and press Play").
- **Tune strip** above the keys: a white rounded box with the tune in big purple letters
  (`F5 F5 F5 E5 F5 C6 F5 E5`), like the banner in the picture. In Automated mode it shows the table's keys and the
  one being played turns yellow; in Manual mode it shows the keys the user has tapped so far (last ~12), with a ✕ to clear.
- **Keyboard:** fills the screen width (16 px side gutter), tall white keys with rounded bottoms and a soft shadow,
  black keys about 60 % as tall, the name label in a small **light blue rounded tag** near the bottom of each white key
  (as in the picture). Black keys get a small label too (C#5, D#5, F#5, G#5, A#5) (owner's choice).
- A pressed key turns yellow (`#ffc107`, the app's highlight colour) and dips slightly (CSS transform), then fades back.
- Phone portrait: keys about 45 px wide and 200 px tall. A "turn your phone sideways for bigger keys" hint shows in
  portrait; in landscape the keys grow to fill the width. Laptop: the same keyboard centred, max ~640 px wide.
- Bootstrap 5.3.3 from the jsDelivr CDN, everything else inline; no build step. Works opened from disk and on GitHub Pages.

## 3. Sound (reused from piano.html)

Copy the sound part of `piano.html` (section "SOUND: recorded piano samples"):

- `ensureCtx()`: the soft piano bus (low-pass 4.2 kHz, −5 dB high shelf at 2.2 kHz, small room echo, gentle compressor).
- Sample loading from `NOTES-TESTER/SAMPLES/piano.js` (FluidR3_GM grand piano, CC BY 3.0), with the lead-in silence cut
  and the peak set to 0.6. **Change for phones:** decode only the 13 samples the mini piano needs (MIDI 72–84) instead
  of all 64, so it is ready in about a second on a phone. (The .js file itself is still downloaded once, ~2 MB.)
- `note(m, when, dur, lvl)`: plays a sample, with the triangle + sine synth as a fallback if the samples are missing.
- The `AudioContext` is created on the **first tap** (phones only allow sound after a user gesture). Until the samples
  are decoded, the synth fallback plays, so the first tap is never silent.

## 4. Manual mode

- **Pointer events** (`pointerdown` / `pointerup` / `pointercancel`) so touch, mouse and pen all work, with
  `touch-action: none` on the keyboard so the page does not scroll or zoom while playing.
- **Several fingers at once** (chords), each pointer tracked by its id.
- A note sounds while the key is held and rings out (0.3 s release, like a sustain pedal) when released.
- **Sliding** a finger across keys plays each new key it reaches (glissando).
- Laptop keys also work: `A W S E D F T G Y H U J K` = C5 … C6 (white row plus black keys above), as a bonus for testing on a PC.
- **📋 Copy to table** button (owner's choice): moves the keys tapped so far into the Automated table, with the time between
  taps (rounded to 50 ms) as the wait, so a user can play a tune by hand and then replay it.

## 5. Automated mode

### Table

| # | Key to press | Wait (ms) | |
|---|---|---|---|
| 1 | F5 ▾ | 400 | 🗑 |
| 2 | F5 ▾ | 400 | 🗑 |
| … | | | |

- The first time it opens, it is filled with the owner's Pehla Nasha tune, **25 rows**
  (owner's choice, instead of 5 plain rows):
  `F5 F5 F5 E5 F5 C6 F5 E5 D5 E5 F5 A5 F5 F5 G5 G5 G5 C5 F5 G5 A5 G5 F5 E5 F5`, with waits from the song's rhythm (2026-11-17: bars 25–31 of the
  5-minute piano arrangement, eighth note = 205 ms; first built with 400 ms each).
- **Key to press:** a drop-down with the 13 keys (C5, C#5, D5 … C6), so no typing on a phone and no invalid names.
  Tapping a piano key while a row's drop-down is focused also fills it (quick entry).
- **Wait (ms):** a number box (`inputmode="numeric"`), whole numbers 50–5000. An empty or invalid value turns the box
  red and disables Play, with a message (same style as the bar-range check in `piano.html`).
- **Meaning of the wait:** the time from pressing this row's key to pressing the next row's key. The last row's wait is
  how long the final note rings. Each note sounds for its wait (capped at 1.5 s, minimum 0.1 s), so short waits give
  short, crisp notes and long waits let a note ring.
- **➕ Add row** below the table: adds a row copying the last row's key and wait. Each row has a 🗑 to delete it
  (at least one row always stays). Rows are numbered.
- **Tune presets** drop-down above the table: "Pehla Nasha" = the 25-note tune above, plus "Empty (5 rows)". Choosing a preset replaces the table (after a confirm if the table was edited).

### Controls

- **▶ Play:** checks the table, then schedules every row on the Web Audio clock (`ctx.currentTime`), not with
  `setTimeout`, so timing stays exact even on a slow phone. A `requestAnimationFrame` loop lights the matching key
  yellow, highlights the current table row and the note in the tune strip, and scrolls the row into view.
- **■ Stop:** stops at once (stops the scheduled sources) and clears the highlights.
- **Speed** 50–150 % (divides every wait) and **🔁 Loop** (starts again after the last row's wait).
- While playing, the table is locked (inputs disabled) and the keys can't be tapped.

### Saving

The table (keys, waits, speed, loop) is saved in `localStorage` (`miniPianoTable`) in a try/catch, so it is still there
next time on the same phone. The page works without it.

## 6. Page structure (one file, `mini-piano.html`)

```
nav
main
  mode switch: [✋ Manual] [🤖 Automated]   (Bootstrap btn-group, remembered in localStorage)
  tune strip
  keyboard (#kbd)
  Automated only: presets, table, ➕ Add row, ▶ Play, ■ Stop, Speed, 🔁 Loop, message line
  sound status line ("🎹 Piano sound ready")
footer: links to index.html, piano.html, contactus.html
```

JS sections: notes table (name ↔ MIDI 72–84), keyboard drawing, sound (copied), manual input, table editing and
validation, scheduler/player, localStorage, `window.__miniPiano` = {press(name), release(name), rows(), setRows(list),
play(), stop()} for headless tests.

## 7. Links and docs

- Add "🎹 Mini Piano" to the footers of `index.html` and `piano.html` (and a card on `contactus.html`).
- Add a `mini-piano.html` row and a short "Mini Piano" section to `.claude/CLAUDE.md`.
- Mark this plan "approved and built" with any changes once it is done.

## 8. Testing

- Headless Chrome (CDP, `--autoplay-policy=no-user-gesture-required`, `--mute-audio`): load the page, set the Pehla
  Nasha preset, press Play, check that the lit keys follow all 25 notes of the tune at the table's times (±30 ms), that
  Add row / delete row / invalid wait / Stop / Loop behave, and that a reload keeps the table.
- Screenshots at 390 px (phone portrait), 844 × 390 (phone landscape) and 1280 px (laptop).
- Opened from disk (`file://`) and over http, to check the samples load in both.
- The owner tries it on a phone after the push.

## 9. Owner's decisions (2026-11-17)

1. **Key range:** only **C5–C6**, as in the picture; no octave buttons. Tunes must fit in C5–C6.
2. **Black keys:** show their names (C#5 …).
3. **Wait meaning:** a row's wait is the time after its key before the next row's key; the last row's wait is how long
   the final note rings.
4. **Default table:** the 25-note Pehla Nasha tune
   `F5 F5 F5 E5 F5 C6 F5 E5 D5 E5 F5 A5 F5 F5 G5 G5 G5 C5 F5 G5 A5 G5 F5 E5 F5`.
5. **Copy to table** in Manual mode: yes.
