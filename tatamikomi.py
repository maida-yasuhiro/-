# -*- coding: utf-8 -*-
u"""
?????f?[?^?̏??ݍ??݂??s??
"""
from scipy import array, ceil, float64, int16, log2, zeros
from scipy import ifft
from scipy.fftpack import fft
# from scipy.io.wavfile import read, write
from scikits.audiolab import wavread, wavwrite
import os

# ========
#  HELPER
# ========

def nextpow2(n):
    return ceil(log2(abs(n)))

def sampling_reverb(signal_array, impulse_response):
    sigL = len(signal_array)
    irL = len(impulse_response)

    new_irL = int((2 ** nextpow2(irL)) * 2) 
    frameL = new_irL / 2
    new_IR = zeros(new_irL, dtype = float64)
    new_IR[: irL] = impulse_response

    frame_num = int(ceil((sigL + frameL) / float(frameL)))
    new_sigL = frameL * frame_num
    new_sig = zeros(new_sigL, dtype = float64)
    new_sig[frameL : frameL + sigL] = signal_array

    ret = zeros(new_sigL - frame_num, dtype = float64) 
    ir_fft = fft(new_IR) 
    for ii in xrange(frame_num - 1):
        s_ind = frameL * ii
        e_ind = frameL * (ii + 2)

        sig_fft = fft(new_sig[s_ind : e_ind]) 
        ret[s_ind : s_ind + frameL] = ifft(sig_fft * ir_fft)[frameL :].real

    print new_irL, sigL, new_sigL
    return ret[: sigL]


def test():
    num = 4
    cur_dir = os.getcwd()
    os.chdir(cur_dir + "/senmendai1/9_ugai_only")
    wav_file = "./%d.wav" %num
    impulse_response_file = cur_dir + "/impulse/3.wav"

    data, fs_sig, fmt = wavread(wav_file)
    impulse_response, fs_ir, fmt2 = wavread(impulse_response_file)
    assert fs_sig == fs_ir, ":("

    reverbed_signal = sampling_reverb(data, impulse_response)

    if max(reverbed_signal) > 1:
        reverbed_signal /= (max(reverbed_signal) * 1.2)

    wavwrite(reverbed_signal, cur_dir + "/senmendai1/new%d.wav" %num, fs = fs_sig)

if __name__ == "__main__":
    test()
