"""
musicdsp.py: the shared toolkit for finding notes in a recording (numpy + scipy only).

The steps, in the order the scripts use them:

    load_wav()          read a WAV, mix to mono, scale to -1..+1, optionally cut start..end
    spectrogram()       STFT: how strong every frequency is in short slices of time
    estimate_tuning()   how many cents sharp or flat the whole recording is
    salience()          for every note (MIDI number) and every slice: its energy plus its harmonics'
    onset_envelope()    spectral flux: how much new energy appears from one slice to the next
    detect_onsets()     peaks in the flux = the moments notes start
    estimate_tempo()    beats per minute from the rhythm of the flux
    estimate_key()      major/minor key from which notes were found (Krumhansl-Kessler profiles)

Analysis wraps them so a script can ask "which notes are sounding between t0 and t1?".
Times are always seconds in the ORIGINAL file, even when only part of it is analysed.
"""
import math
import re

import numpy as np
from scipy.io import wavfile
from scipy.ndimage import median_filter
from scipy.signal import find_peaks, resample_poly, stft

# --------------------------------------------------------------------------------- note names
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def midi_to_name(m):
    """60 -> 'C4' (sharps, the way song-library.js writes them)."""
    return NOTE_NAMES[m % 12] + str(m // 12 - 1)


def name_to_midi(txt):
    """'C4' -> 60, 'F#4' -> 66, 'Bb3' -> 58 (also accepts the ♯ and ♭ signs)."""
    mt = re.fullmatch(r'([A-Ga-g])([#b♯♭]?)(-?\d)', txt.strip())
    if not mt:
        raise ValueError('unknown note name %r' % txt)
    pc = NOTE_NAMES.index(mt.group(1).upper())
    pc += {'#': 1, '♯': 1, 'b': -1, '♭': -1}.get(mt.group(2), 0)
    return (int(mt.group(3)) + 1) * 12 + pc


def midi_to_hz(m, cents=0.0):
    """Frequency of MIDI note m, shifted by the recording's tuning offset in cents."""
    return 440.0 * 2.0 ** ((m - 69) / 12.0 + cents / 1200.0)


# --------------------------------------------------------------------------------- audio in
def load_wav(path, start=None, end=None, target_sr=22050):
    """Read a WAV file as mono float32 in -1..+1, resampled to target_sr.

    Returns (x, sr, offset) where offset is the start time in seconds, so that
    sample i of x is at time offset + i / sr in the original file.
    22 050 Hz keeps everything up to 11 kHz, plenty for pitch and onsets, and
    halves the work compared with 44.1 / 48 kHz."""
    sr, x = wavfile.read(path)
    if x.dtype == np.int16:
        x = x / 32768.0
    elif x.dtype == np.int32:
        x = x / 2147483648.0
    elif x.dtype == np.uint8:
        x = (x - 128) / 128.0
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)                     # stereo -> mono
    s = int(round((start or 0) * sr))
    e = len(x) if end is None else min(len(x), int(round(end * sr)))
    x = x[s:e]
    offset = s / float(sr)
    if target_sr and sr != target_sr:
        g = math.gcd(int(sr), int(target_sr))
        x = resample_poly(x, target_sr // g, sr // g)
        sr = target_sr
    return x.astype(np.float32), sr, offset


# --------------------------------------------------------------------------------- STFT
def spectrogram(x, sr, win=4096, hop=512, nfft=None, fmax=None):
    """Magnitude STFT with a Hann window.

    Returns (freqs, times, mag) with mag[freq_bin, frame]. times are frame CENTRES
    in seconds from the start of x. nfft > win zero-pads, which gives finer bins
    (smoother peaks) but not finer true resolution."""
    f, t, Z = stft(x, fs=sr, window='hann', nperseg=win, noverlap=win - hop,
                   nfft=nfft or win, boundary='zeros', padded=True)
    mag = np.abs(Z).astype(np.float32)
    if fmax:
        keep = f <= fmax
        f, mag = f[keep], mag[keep]
    return f, t, mag


# --------------------------------------------------------------------------------- tuning
def estimate_tuning(mag, freqs, fmin=100.0, fmax=2000.0, every=2):
    """How far (in cents, -50..+50) the recording sits from A = 440 Hz.

    For every few frames, find the spectral peaks, measure each peak's exact
    frequency by fitting a parabola through the log magnitudes of 3 bins, and see
    how many cents it is from the nearest equal-tempered note. The answer is the
    loudness-weighted CIRCULAR mean (so +49 and -49 cents average to +-50, not 0)."""
    band = np.where((freqs > fmin) & (freqs < fmax))[0]
    df = freqs[1] - freqs[0]
    logm = np.log(mag + 1e-9)
    sin_sum = cos_sum = 0.0
    for j in range(0, mag.shape[1], every):
        col = mag[band, j]
        top = col.max()
        if top < 1e-4:
            continue
        peaks, _ = find_peaks(col, height=top * 0.15)
        for p in peaks:
            k = band[p]
            if k <= 0 or k >= len(freqs) - 1:
                continue
            a, b, c = logm[k - 1, j], logm[k, j], logm[k + 1, j]
            den = a - 2 * b + c
            d = 0.5 * (a - c) / den if den != 0 else 0.0
            f = freqs[k] + d * df
            if f <= 0:
                continue
            dev = 1200 * math.log2(f / 440.0)
            ang = 2 * math.pi * dev / 100.0
            w = float(mag[k, j])
            sin_sum += w * math.sin(ang)
            cos_sum += w * math.cos(ang)
    if sin_sum == 0 and cos_sum == 0:
        return 0.0
    return math.atan2(sin_sum, cos_sum) * 100.0 / (2 * math.pi)


# --------------------------------------------------------------------------------- salience
def salience(mag, freqs, lo, hi, cents=0.0, n_harm=6, decay=0.8, tol_cents=35.0):
    """Harmonic salience: S[note - lo, frame].

    A note's score = its own energy + decay * 2nd harmonic + decay^2 * 3rd + ...
    (each taken as the strongest bin within +-tol_cents of where it should be).
    The real note collects energy from ALL its harmonics, so it beats the overtone
    that happens to be the loudest single peak. Magnitudes are square-rooted first
    so one very loud partial can't dominate."""
    comp = np.sqrt(mag)
    S = np.zeros((hi - lo + 1, mag.shape[1]), dtype=np.float32)
    r = 2.0 ** (tol_cents / 1200.0)
    for i, m in enumerate(range(lo, hi + 1)):
        f0 = midi_to_hz(m, cents)
        for h in range(1, n_harm + 1):
            fc = f0 * h
            if fc * r > freqs[-1]:
                break
            k0 = np.searchsorted(freqs, fc / r)
            k1 = max(np.searchsorted(freqs, fc * r, side='right'), k0 + 1)
            S[i] += (decay ** (h - 1)) * comp[k0:k1].max(axis=0)
    return S


# --------------------------------------------------------------------------------- onsets
def onset_envelope(x, sr, win=1024, hop=128, fmin=30.0, fmax=8000.0):
    """Spectral flux: for each short frame, the total INCREASE in log-magnitude
    over the previous frame (decreases are ignored). Peaks = note starts.
    Returns (env normalised to 0..1, times)."""
    f, t, mag = spectrogram(x, sr, win=win, hop=hop)
    band = (f >= fmin) & (f <= fmax)
    L = np.log1p(100.0 * mag[band])
    flux = np.maximum(np.diff(L, axis=1), 0.0).sum(axis=0)
    flux = np.concatenate([[0.0], flux])
    peak = flux.max()
    return (flux / peak if peak > 0 else flux), t


def detect_onsets(env, times, delta=0.06, min_gap=0.07, median_window=0.5):
    """Pick the flux peaks that stand out: higher than the local median by delta,
    and at least min_gap seconds apart. Returns (onset_times, strengths)."""
    hop_s = times[1] - times[0]
    size = max(3, int(median_window / hop_s) | 1)
    base = median_filter(env, size=size, mode='nearest')
    peaks, _ = find_peaks(env, height=base + delta, distance=max(1, int(min_gap / hop_s)))
    return times[peaks], env[peaks]


# --------------------------------------------------------------------------------- tempo
def tempo_candidates(env, times, bpm_min=60, bpm_max=200, prior_bpm=110, top=3):
    """Likely tempos, best first: [(bpm, score), ...].

    Autocorrelation of the onset envelope says at which lags the rhythm repeats.
    A comb adds the lags at 2x, 3x and 4x the beat too (a real beat repeats at all
    of them), and a gentle preference for tempos near prior_bpm. Tempo is
    genuinely ambiguous (half and double speed fit the same notes), so look at the
    candidates and pass --tempo if the first one is wrong."""
    hop_s = times[1] - times[0]
    e = env - env.mean()
    n = len(e)
    spec = np.fft.rfft(e, 2 * n)
    ac = np.fft.irfft(spec * np.conj(spec))[:n]
    lags = range(max(1, int(60.0 / bpm_max / hop_s)), min(n - 1, int(60.0 / bpm_min / hop_s)) + 1)
    scores = {}
    for lag in lags:
        comb = sum(ac[k * lag] / k for k in range(1, 5) if k * lag < n)
        bpm = 60.0 / (lag * hop_s)
        scores[lag] = comb * math.exp(-0.5 * (math.log2(bpm / prior_bpm) / 0.8) ** 2)
    out = []
    for lag in sorted(scores, key=scores.get, reverse=True):
        bpm = 60.0 / (lag * hop_s)
        if all(abs(bpm - b) / b > 0.04 for b, _ in out):   # skip near-duplicates of a peak already taken
            out.append((bpm, float(scores[lag])))
        if len(out) == top:
            break
    return out or [(float(prior_bpm), 0.0)]


def estimate_tempo(env, times, **kw):
    """The most likely tempo in BPM (see tempo_candidates)."""
    return tempo_candidates(env, times, **kw)[0][0]


# --------------------------------------------------------------------------------- key
_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
KEY_NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']


def estimate_key(midis, weights=None):
    """Krumhansl-Kessler key finding: correlate the pitch-class histogram of the
    notes found with the 24 major/minor key profiles. Returns e.g. 'Bb minor'."""
    hist = np.zeros(12)
    for i, m in enumerate(midis):
        hist[m % 12] += 1.0 if weights is None else weights[i]
    if hist.sum() == 0:
        return '?'
    best, name = -2.0, '?'
    for tonic in range(12):
        for prof, mode in ((_MAJOR, 'major'), (_MINOR, 'minor')):
            r = np.corrcoef(hist, np.roll(prof, tonic))[0, 1]
            if r > best:
                best, name = r, '%s %s' % (KEY_NAMES[tonic], mode)
    return name


# --------------------------------------------------------------------------------- one object
class Analysis:
    """Everything about one clip, computed once.

        a = Analysis('song.wav', lo='C3', hi='C6')
        a.cents                  tuning offset
        a.notes_between(t0, t1)  salience per note, averaged over that time
        a.onsets, a.onset_strength, a.tempo
    """

    def __init__(self, path, start=None, end=None, lo='C3', hi='C6', cents=None,
                 win=4096, hop=256, n_harm=6, onset_delta=0.06, onset_min_gap=0.07, log=None):
        say = log or (lambda *_: None)
        self.path = path
        self.lo = name_to_midi(lo) if isinstance(lo, str) else lo
        self.hi = name_to_midi(hi) if isinstance(hi, str) else hi
        self.x, self.sr, self.offset = load_wav(path, start, end)
        self.duration = len(self.x) / self.sr
        say('loaded %s: %.2f s (from %.2f s), %d Hz mono' % (path, self.duration, self.offset, self.sr))

        # Long windows for pitch (fine frequency detail) ...
        self.freqs, t, mag = spectrogram(self.x, self.sr, win=win, hop=hop, nfft=2 * win, fmax=6000)
        self.times = t + self.offset
        self.cents = estimate_tuning(mag, self.freqs) if cents is None else float(cents)
        say('tuning offset: %+.1f cents' % self.cents)
        self.S = salience(mag, self.freqs, self.lo, self.hi, self.cents, n_harm=n_harm)
        say('salience: %d notes (%s..%s) x %d frames' % (self.S.shape[0], midi_to_name(self.lo), midi_to_name(self.hi), self.S.shape[1]))

        # ... short windows for timing.
        self.env, et = onset_envelope(self.x, self.sr)
        self.env_times = et + self.offset
        self.onsets, self.onset_strength = detect_onsets(self.env, self.env_times, delta=onset_delta, min_gap=onset_min_gap)
        self.tempos = tempo_candidates(self.env, self.env_times)
        self.tempo = self.tempos[0][0]
        say('onsets: %d, tempo about %.0f BPM (other candidates: %s)' % (
            len(self.onsets), self.tempo, ', '.join('%.0f' % b for b, _ in self.tempos[1:]) or 'none'))

    def notes_between(self, t0, t1):
        """Mean salience of every note over frames whose centres fall in [t0, t1]."""
        sel = (self.times >= t0) & (self.times <= t1)
        if not sel.any():
            sel = np.zeros(len(self.times), bool)
            sel[int(np.argmin(np.abs(self.times - (t0 + t1) / 2)))] = True
        return self.S[:, sel].mean(axis=1)

    def ranked(self, t0, t1, top=5):
        """[(midi, score), ...] strongest first."""
        v = self.notes_between(t0, t1)
        order = np.argsort(v)[::-1][:top]
        return [(self.lo + int(i), float(v[i])) for i in order]

    def sal(self, vec, m):
        return float(vec[m - self.lo]) if self.lo <= m <= self.hi else 0.0
