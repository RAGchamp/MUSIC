/* =====================================================================
   SONG LIBRARY for index.html (Music Practice App)
   ---------------------------------------------------------------------
   Every song in the "Choose a song" drop-down comes from this list.
   The audio files live in this same folder (REFERENCE-AUDIO-FILES).

   To add a song:
     1. Put its .wav (or .mp3) file in this folder.
     2. Copy one of the entries below and change it.

   Fields:
     title   name shown in the drop-down
     audio   file name in this folder (leave out for a synth-only song)
     key     shown under the song name
     inst    the instrument the song is played on: 'piano' or 'guitar' (a suggestion, you can pick either)
     tempo   beats per minute; only used when the notes have no times
     notes   one line per note:   'time   notes   beats   label'
               time   seconds into the audio file when the note starts ('-' if you have no audio)
               notes  note names joined by +, e.g. E5+B4 (a double stop) or C4 (a single note)
                      start with ~ for a slide into the note, ^ for a hammer-on / pull-off
                      add @string to put a note on a particular guitar string (e B G D A E), e.g. G4@G
               beats  how long the note lasts in beats (0.5 = eighth note, 1 = quarter note)
               label  optional, e.g. a chord name
   ===================================================================== */
window.SONG_LIBRARY = [
  {
    title: 'Inteha Ho Gayi: guitar intro (Sharaabi)',
    audio: 'SONG-1-inteha-ho-gayi-start.wav',
    key: 'E minor',
    inst: 'guitar',
    tempo: 154,
    // Note start times measured from the recording. Most notes are double stops:
    // the same fret on the high-e and B strings.
    notes: [
    ' 0.61  E4+B3+G3+E3+B2+E2        2  Em chord',
    ' 1.43  B4+F#4                 0.5',
    ' 1.62  B4+F#4                   1',
    ' 2.10  ~E5+B4                   1',
    ' 2.46  E5+B4                  0.5',
    ' 2.71  E5+B4                    1',
    ' 3.01  E5+B4                  3.5',
    ' 4.45  D5+A4                  0.5',
    ' 4.72  E5+B4                  0.5',
    ' 4.95  E5+B4                  0.5',
    ' 5.11  E5+B4                    1',
    ' 5.51  G5+D5                  0.5',
    ' 5.79  E5+B4                  0.5',
    ' 6.01  G5+D5                  0.5',
    ' 6.19  E5+B4                  0.5',
    ' 6.35  E5+B4                    1',
    ' 6.68  E5+B4                    1',
    ' 7.13  D5+A4                  0.5',
    ' 7.30  D5+A4                  0.5',
    ' 7.49  ~E5+B4                 0.5',
    ' 7.72  E5+B4                  0.5',
    ' 7.92  ~D5+A4                 0.5',
    ' 8.10  D5+A4                  0.5',
    ' 8.32  ~B4+F#4                0.5',
    ' 8.51  B4+F#4                   4',
    '10.16  G4@G                   0.5',
    '10.31  B4@B                     1',
    '10.63  E5                     1.5',
    '11.23  B4+F#4                 0.5',
    '11.53  D5+A4                  0.5',
    '11.78  D5+A4                  0.5',
    '11.92  E5+B4                  0.5',
    '12.18  E5+B4                  0.5',
    '12.37  ~D5+A4                 0.5',
    '12.54  D5+A4                  0.5',
    '12.69  B4+F#4                 0.5',
    '12.95  B4+F#4                 0.5',
    '13.13  B4+F#4                 0.5',
    '13.35  B4+F#4                   1',
    '13.79  B4+F#4                   1',
    '14.10  ~A4+E4                 0.5',
    '14.21  A4+E4                    1',
    '14.52  A4+E4                  0.5',
    '14.76  A4+E4                    1',
    '15.24  A4+E4                    3',
    '16.45  A4+E4                  0.5',
    '16.68  A4+E4                  0.5',
    '16.86  A4+E4                  0.5',
    '17.03  B4+F#4                   1',
    '17.36  B4+F#4                 0.5',
    '17.58  D5+A4                  0.5',
    '17.78  D5+A4                  0.5',
    '17.95  D5+A4                  0.5',
    '18.09  E5+B4                  0.5',
    '18.29  E5+B4                  0.5',
    '18.48  E5+B4                  0.5',
    '18.66  ~D5+A4                 0.5',
    '18.79  D5+A4                  0.5',
    '18.95  D5+A4                  0.5',
    '19.12  ~B4+F#4                0.5',
    '19.24  B4+F#4                 0.5',
    '19.41  B4+F#4                 0.5',
    '19.58  ~A4+E4                 0.5',
    '19.69  A4+E4                  0.5',
    '19.88  A4+E4                  0.5',
    '20.02  B4+F#4                 1.5',
    '20.70  ^E4+B3                 0.5',
    '20.84  E4+B3                    3',
    ]
  }
];
