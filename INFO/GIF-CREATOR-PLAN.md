# GIF Creator: plan

**Status:** approved and built (2026-11-20): `GIF-CREATOR/gif.html`. Built as planned, except:
- the GIF encoder is a small one written for the page (median-cut palette, LZW, changed-rectangle frames with
  transparency) instead of gifenc, so there is no copied library at all;
- the preview is drawn through the same canvas path as the GIF (so it is exactly what the GIF will show);
- the credit line was replaced (owner, 2026-11-20) by a drawn red "🎞️ Create a Gif" button with the page's address
  `ragchamp.github.io/MUSIC/GIF-CREATOR/gif.html` (a GIF can't hold a link); the tick box now shows/hides that;
- **added later the same day (owner's request): a video with sound.** A GIF can't hold audio, so a new step 4 records up
  to 10 s of the user's **voice** (owner's choice) and step 5 has **🎬 Create video with sound**: a 10 s MP4 (always 10 s,
  owner's choice; the animation loops under the voice), recorded from a canvas with `MediaRecorder` (WebM where MP4 isn't supported);
- a photo face and a 🧚 Fairies choice were added later the same day and then **removed at the owner's request**
  (keep it simple: monkeys only);
- the disco ball and spotlights appear only in Dance party; Chiku's banana only in Dance party, the trophy in Congratulations.
Checked headless: each theme at 540 × 600, 5 s, 12.5 fps = 63 frames, 2.2–3.0 MB, ~3.5 s to make; 360 × 400, 3 s ≈ 1 MB.

## 1. Goal

A new page, `GIF-CREATOR/gif.html` (`C:\Daya\RAGchamp\MUSIC\GIF-CREATOR\gif.html`, live at
https://ragchamp.github.io/MUSIC/GIF-CREATOR/gif.html), that makes a short animated GIF of **Chiku and Miku**, the two
monkeys in red velvet suits from the Rani Rani page (`MUSIC-PROD/SONG-2.html`), to send to friends (WhatsApp, email, social media).

The user:
1. picks one of **5 themes** (one of them **💋 Throwing kisses**),
2. types a **message of up to 50 characters** (e.g. "Love you Mum!"),
3. watches a live preview,
4. presses **Create GIF** and saves, downloads or shares the file.

Everything happens in the browser. Nothing is uploaded. It works opened from disk (`file://`) and on GitHub Pages.

## 2. The sample GIF (what we learnt from it)

`GIF-CREATOR/Gifs/GIF-1-throwing-kisses.gif`: 540 × 602 px (portrait), 120 frames at 80 ms (12.5 fps), **10 s**, loops,
**10.7 MB**. Frame 1 is the Rani Rani stage (Chiku with the banana, Miku with the flower, hearts, coloured floor tiles,
credit line "Rani Rani · Lyrics & Music: Daya · Voice: AI" at the bottom). The other frames are an **AI-made video** in a
different, smoother cartoon style: the monkeys close their eyes, blow kisses from their hands, red hearts and sparkles fly
between them, then they smile and wave.

What this means for the app:
- The app draws the monkeys with the SVG code from SONG-2.html, so its GIFs look like **frame 1**, not like the AI video.
  The kiss theme gets a new "blow a kiss" move drawn in the same SVG style (section 6).
- The sample is too big to send easily (WhatsApp and email prefer a few MB). Flat SVG cartoons compress much better than
  video frames, so the app aims for **under 3 MB** (section 8).
- Format to copy: portrait (about 9:10), black stage, floor tiles at the bottom, credit line at the very bottom, seamless loop.

## 3. Look (like recorder.html)

Same layout and CSS as `recorder.html`:
- Sticky top nav (`#04264d`, `#ffd60a`, `../logo.svg`, tagline "Music Practice App"); slim one-line nav on phones.
- Title **🎞️ GIF Creator** and a one-line hint, with a "Back to Song Practice" link.
- **Step cards** (`.step-card`, uniform 2px `#c9d3e3` border, yellow numbered circle `.step-num`).
- Theme choice uses the `.mode-opt` boxes (big emoji, bold name, small grey line, blue outline when chosen).
- Blue gradient `.prompt` box for status ("Drawing frame 34 of 75…"), `.now-card`s for GIF size / frames / length,
  `.big-play` buttons, `.file-box` for the save folder, dark blue footer.
- Bootstrap 5.3.3 from jsDelivr; everything else inline; no build step.

## 4. Page steps

**Step 1: Choose a theme.** Five `.mode-opt` boxes (two columns on laptop, one on phones):

| Theme | Monkeys do | Extras on the stage | Default message |
|---|---|---|---|
| 💋 **Throwing kisses** | close their eyes, pucker, blow kisses from the hand towards each other | red/pink hearts fly from the hands, sparkles, pink floor tiles | "Sending you kisses!" |
| 🎂 **Happy Birthday** | clap, then hands-up wave | a cake with candles between them (flames flicker), balloons rise, confetti | "Happy Birthday!" |
| 💃 **Dance party** | the Rani Rani moves (clap, wave, scratch, punch, swim) on the beat | disco ball, spotlights, neon sign, floor tiles flash | "Let's dance!" |
| 🙏 **Thank you** | bow (head and body tilt), namaste hands | flower petals fall, warm gold glow | "Thank you so much!" |
| 🎉 **Congratulations** | jump with both arms punching up | confetti bursts, gold stars, a trophy held up by Chiku | "Congratulations!" |

**Step 2: Your message.**
- Text box, `maxlength="50"`, live counter "23 / 50" (red at 50). Counts real characters, so an emoji counts as 1.
- Choosing a theme fills in its default message only if the box is empty or still holds another theme's default.
- Options: **Position** (top / bottom), **Colour** (yellow `#ffd60a` default, white, pink, green neon), **Show credit line**
  (tick box, on by default: "Rani Rani · Lyrics & Music: Daya · Voice: AI").
- Long messages wrap onto two lines and the font shrinks to fit the width.

**Step 3: Preview.** The live SVG stage at the chosen size, looping exactly as the GIF will. Controls: ▶ / ❚❚, and
**Length** (3 / 5 / 8 s, default 5 s), **Size** (540 × 600 portrait, default; 480 × 480 square; 360 × 400 small), **Speed** (frames per
second 10 / 12.5 / 15, default 12.5 like the sample).

**Step 4: Create and save.**
- **🎞️ Create GIF** draws every frame, then encodes; a progress bar and the prompt show "Drawing frame N of M", then "Encoding…".
  ■ Cancel stops it.
- The finished GIF is shown as an `<img>` with its file size, frames and length in `.now-card`s (warning in orange above 5 MB).
- **💾 Save** writes `GIF-<n>-<theme>.gif` (e.g. `GIF-2-happy-birthday.gif`; n = next free number) into a folder chosen once with
  `showDirectoryPicker` (like recorder.html; handle kept in IndexedDB `gif-creator` / `saveDir`), suggested folder
  `GIF-CREATOR/Gifs`. **📁 Choose folder…** re-picks it.
- **⬇ Download instead** for browsers without the File System Access API (phones, Firefox, Safari).
- **📤 Share** (phones): `navigator.share({ files:[gifFile] })` opens the phone's share sheet (WhatsApp, etc.); hidden where unsupported.

## 5. Reusing the SONG-2.html animation

Like the other pages in this repo, the code is **copied** into gif.html (no shared .js file), then changed:
- **Copied as is:** `el()`, `f1`, `lerpP`, `curve`, `smooth`, `frac`, the `#velvet` gradient, `makeMonkey()` (head, cap, flower,
  banana, eyes with blinking lids, arms, legs, yellow shoes, shadow), the hearts, the floor tiles (`TILE_COLORS`),
  the disco ball and spotlights.
- **Changed:**
  - **No audio.** SONG-2 drives the beat from `player.currentTime`, `BEAT`, `PHASE` and `ENERGY`. gif.html uses a
    **clock function** `drawAt(t)` instead: the beat is a fixed tempo per theme (Dance party keeps 192 bpm), energy is fixed
    (e.g. 0.8), and `T`/`now` come from `t`, not `performance.now()`.
  - **Deterministic:** every `Math.random()` (hearts, confetti, blink times) uses a seeded random generator, so the preview
    and the GIF show exactly the same thing and the same settings always give the same GIF.
  - **Seamless loop:** the GIF length is a whole number of beats and of move cycles; hearts/petals/confetti positions are
    computed from `t mod length` (they wrap round), so the last frame flows into the first.
  - **Fixed stage size:** `layout()` is called with the GIF size (540 × 600, 480 × 480 or 360 × 400) instead of the screen.
  - **Theme moves:** `MOVES` gets new entries (blow kiss, namaste, bow, cheer jump); each theme is a short **timeline**
    (list of `{ from, to, move }`) instead of "a new move every 16 half-beats".
  - New face parts: closed happy eyes (curved lids), puckered mouth "o", rosy cheeks (already there, made stronger).
  - Speech bubbles ("Hey!", "Rani!") are left out; the user's message replaces them.

## 6. The 💋 Throwing kisses theme (in detail)

A 5 s loop (default), both monkeys facing each other a little (heads tilted inwards):
1. 0–1 s: gentle sway, eyes open, smiling (like frame 1 of the sample).
2. 1–2 s: one hand goes to the mouth, eyes close (lids down, curved), mouth becomes a small "o".
3. 2–3 s: the hand swings out towards the other monkey; **3–5 hearts** pop from the hand and fly in an arc to the other
   monkey's face, growing then fading, with small white/pink sparkles. Chiku first, Miku answers half a beat later.
4. 3–4.5 s: both blow a second kiss together; a big heart rises between them and bursts into small hearts.
5. 4.5–5 s: back to smiling, ready to loop.

Background: black stage, slow pink hearts rising (as in SONG-2), floor tiles in pinks and reds. The ready-made sample
`GIF-1-throwing-kisses.gif` stays in `Gifs/` and can be offered as a "ready-made" download (see question 1).

## 7. Drawing the frames

For each frame i (t = i / fps):
1. `drawAt(t)` updates the SVG (the same code the preview uses).
2. The SVG is serialised (`XMLSerializer`) into a Blob URL and drawn into an `Image`, then onto a `<canvas>` of the GIF size.
3. The message and the credit line are drawn **on the canvas** with `fillText` (thick black outline + fill, like the
   thumbnails), because an SVG drawn as an image cannot load web fonts and canvas handles emoji better.
4. `getImageData` gives the RGBA pixels for the encoder.

About 60–100 frames per GIF; on the owner's slow PC (Pentium N5030) expected 5–15 s in total. Frames are drawn one per
`setTimeout(0)` so the page stays responsive and Cancel works.

## 8. Making the GIF file (size)

- **Encoder:** the small MIT-licensed **gifenc** library (mattdesl/gifenc), **copied inline** into gif.html with its licence
  comment, so it works on `file://` with no web worker (gif.js needs a worker file from the same origin, which a
  `file://` page can't load).
- **One palette for the whole GIF** (`quantize` on pixels sampled from ~10 frames, 128–256 colours), so colours don't flicker
  between frames and the file is smaller. Black is kept as a palette entry so the background stays pure black.
- Frame delay 80 ms (12.5 fps) by default; loop forever (`repeat: 0`).
- **Expected size:** 540 × 600, 5 s, 62 frames: roughly 1.5–3 MB (flat colours, a lot of unchanged black). The small size
  (360 × 400) about half that. If a GIF is over 5 MB, a hint suggests the small size or a shorter length.
- Later, if needed: only encode the changed rectangle of each frame (sub-frame boxes) to shrink files further.

## 9. Phones

- Works at 390 px: theme boxes stack, the preview fits the width (CSS scale; the GIF size does not change), buttons wrap.
- Encoding on a phone is fine for the small size; the normal size may take ~20 s on older phones (the prompt says so).
- Save = Download or Share (no folder picker on phones).

## 10. Testing

- `window.__gifCreator` = { themes, setTheme(id), setMessage(text), drawAt(t), frames(), create(opts), lastGif, state } for
  headless tests.
- Headless Chrome checks (as for the other pages):
  - every theme draws without errors for t = 0 … length; the first and last frames match closely (seamless loop);
  - message limit: 51 characters can't be typed; 50 with emoji wraps and fits;
  - a GIF is made for each theme at both sizes; it decodes (Pillow: frame count, delay 80 ms, loop 0) and is under 3 MB at 540 × 600, 5 s;
  - the same settings give a byte-identical GIF twice (seeded random);
  - screenshots at 390 px and 1280 px; no sideways scroll on the phone.

## 11. Owner's decisions (2026-11-20)

1. **Kiss theme:** drawn fresh in the SONG-2 SVG style (message can be added, small file), **and** the ready-made
   `Gifs/GIF-1-throwing-kisses.gif` is offered as an extra "⬇ Ready-made kiss GIF" download in that theme's box.
2. **Themes:** as planned: 💋 Throwing kisses, 🎂 Happy Birthday, 💃 Dance party, 🙏 Thank you, 🎉 Congratulations.
3. **Credit line:** on by default; the user can untick it.
4. **Sizes:** three: portrait 540 × 600 (default), **square 480 × 480**, small 360 × 400.
5. **Message:** the user chooses position (top / bottom) and colour (yellow, white, pink, neon green).
6. **Links:** from the **index.html footer** and from **SONG-2.html** (a "🎞️ Create a Gif" button under the
   dance stage). Not SITE-MAP.html or contactus.html for now.
7. **Saved GIFs:** committed to the public repo like the WAVs (`GIF-CREATOR/Gifs/`, including the 10.7 MB sample), so the
   ready-made kiss download also works on the live site.
