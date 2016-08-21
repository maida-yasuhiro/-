import numpy as np
from numpy import random
import scipy.fftpack
import matplotlib.pyplot as plt
import wave

def white_noise(length, f_s=44100):
    sample = length * f_s
    time_step = 1. / f_s
    time_arr = np.arange(sample) * time_step
    noise = random.randn(time_arr.size)
    return noise

def save_wave(data, bit, fs, filename):
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(data)
    wf.close()

if __name__ == "__main__":
    f_s = 44100 # sample rate
    length = 11  # length of white noise

    noise = white_noise(length, f_s)
    fft_noise = scipy.fftpack.fft(noise)
    fft_noise = scipy.fftpack.fftshift(fft_noise)
    spectrum_noise = np.abs(fft_noise)**2

#    print(noise)
    freqs = scipy.fftpack.fftfreq(f_s * length, d=1./f_s)
    freq_axis = scipy.fftpack.fftshift(freqs)

    plt.subplot(211)
    plt.plot(np.arange(length * f_s), noise)
    plt.ylim(min(noise), max(noise))
    plt.title("White Noise")

    plt.subplot(212)
    plt.plot(freq_axis[freq_axis.size//2:], spectrum_noise[freq_axis.size//2:])
    plt.ylim(min(spectrum_noise), max(spectrum_noise))
    plt.title("Power Spectrum of White Noise")

#    plt.show()

    save_wave(noise, 5000, 16, "test.wav")

