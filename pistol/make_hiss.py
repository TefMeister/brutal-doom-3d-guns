# The hand cannon's steam hiss, made from scratch (filtered noise), so it is ours to ship with no licence to check.
# Tefa, 2026-10-18: "we gotta get some hisss sounds for that". Three hisses, one per heat band of the heat collector:
# a short soft one when it is nearly cold, a long loud bright one when it is hottest. Numbers: HISS below.
# Run: python make_hiss.py   -> sounds/hiss_low.wav, hiss_mid.wav, hiss_high.wav (22050 Hz, mono, 16-bit).
import os
import wave

import numpy as np

RATE = 22050
HISS = {   # name: (length s, loudness 0-1, brightness = low-pass cutoff Hz, sputter 0-1)
    'low': (0.35, 0.35, 5000, 0.5),
    'mid': (0.85, 0.6, 7000, 0.35),
    'high': (1.6, 0.9, 9500, 0.25),
}
HIGH_PASS_HZ = 1200       # takes the rumble out, leaving the hiss
ATTACK_S = 0.015          # how fast the steam bursts out
TAIL = 0.45               # share of the length spent fading out
PRESSURE_DROP = 0.35      # how much quieter the end of the hiss is than its start
SPUTTER_HZ = 30           # how fast the steam sputters
SEED = 2016


def one_pole(x, cutoff):
    """A gentle low-pass filter."""
    a = np.exp(-2 * np.pi * cutoff / RATE)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def hiss(length, loud, bright, sputter, rng):
    n = int(length * RATE)
    noise = rng.uniform(-1, 1, n)
    x = noise - one_pole(noise, HIGH_PASS_HZ)                  # high-pass
    x = one_pole(one_pole(x, bright), bright)                   # soften the top
    t = np.arange(n) / RATE
    env = np.minimum(1, t / ATTACK_S)                           # burst in
    fade = max(1, int(n * TAIL))
    env[-fade:] *= np.linspace(1, 0, fade) ** 2                  # die away
    env *= 1 - PRESSURE_DROP * t / length                      # pressure dropping
    flutter = one_pole(rng.uniform(-1, 1, n), SPUTTER_HZ)       # the steam sputtering
    flutter /= max(1e-9, np.abs(flutter).max())
    env *= 1 + sputter * flutter
    x *= env
    return x / max(1e-9, np.abs(x).max()) * loud


def write(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(SEED)
    for name, spec in HISS.items():
        path = os.path.join(out, 'hiss_%s.wav' % name)
        write(path, hiss(*spec, rng))
        print(path)


if __name__ == '__main__':
    main()
