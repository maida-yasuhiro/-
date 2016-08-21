#coding:utf-8
import wave
import numpy as np
import scipy.fftpack
from pylab import *

if __name__ == "__main__" :

#    wf = wave.open("white.wav" , "r" ) # 元
#    wf = wave.open("test1.wav" , "r" ) # 元
    wf = wave.open("rec_white_noise.wav" , "r" ) # noise除去なし
#    wf = wave.open("rec_white_noise1.wav" , "r" ) # noise除去あり
#    wf = wave.open("rec_white_noise_nasi.wav" , "r" )
#    wf = wave.open("rec_white_noise2.wav" , "r" )
#    wf = wave.open("./musicdata/1_mizuoto1/1.wav" , "r" )
#    wf = wave.open("rec_white_noise.wav" , "r" )
    fs = wf.getframerate()  # サンプリング周波数
    x = wf.readframes(wf.getnframes())
#    x = frombuffer(x, dtype= "int16") / 32768.0  # -1 - +1に正規化
    x = frombuffer(x, dtype= "int16") 
    print (x)
    wf.close()

    start = 0  # サンプリングする開始位置
    N = 2**8    # FFTのサンプル数

    X = np.fft.fft(x[start:start+N])  # FFT
#    X = scipy.fftpack.fft(x[start:start+N])         # scipy版

    freqList = np.fft.fftfreq(N, d=1.0/fs)  # 周波数軸の値を計算
#    freqList = scipy.fftpack.fftfreq(N, d=1.0/ fs)  # scipy版

    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]  # 振幅スペクトル
    phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in X]    # 位相スペクトル

    # 波形を描画
    subplot(211)  # 3行1列のグラフの1番目の位置にプロット
    plot(range(start, start+N), x[start:start+N])
#    axis([start, start+N, -1.0, 1.0])
    xlabel("time [sample]")
    ylabel("amplitude")

    # 振幅スペクトルを描画
    subplot(212)
    plot(freqList, amplitudeSpectrum, marker= 'o', linestyle='-')
#    axis([-30000, 30000, 0, 750000])
    xlabel("frequency [Hz]")
    ylabel("amplitude spectrum")

    savefig('./fit_nasi.png', dpi=150)
#    savefig('./fit_ari.png', dpi=150)
#    savefig('./fit_moto.png', dpi=150)

#    # 位相スペクトルを描画
#    subplot(313)
#    plot(freqList, phaseSpectrum, marker= 'o', linestyle='-')
#    axis([0, fs/2, -np.pi, np.pi])
#    xlabel("frequency [Hz]")
#    ylabel("phase spectrum")

    show()
