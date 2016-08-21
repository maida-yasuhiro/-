# -*- coding: utf-8 -*-
u"""
以下のことを実行する
1.生活音を取得し、リアルタイムで音声を分類する
2.分類内容の結果に応じて、音声合成による出力を行う
"""

# 自作ライブラリ
import features
import eval_model

# 外部ライブラリ
import os
import time
import wave
import pyaudio
import datetime
import scipy
import numpy as np
import glob
from scipy.io import wavfile
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.utils import resample

# モノラルで約1Hzでフーリエ変換を行う
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = RATE * 3  # 何秒ごとに生活音を取得する
RECORD_SECONDS = 50  # アプリケーションの実行時間[s]

# ディレクトリ
cur_dir = os.getcwd()
STREAM_DIR = cur_dir + "/streamdata"
#DATA_DIR = cur_dir + "/musicdata"
DATA_DIR = cur_dir + "/senmendai1"
CLASS_DIR = cur_dir + "/class_name"
TALK_DIR = cur_dir + "/talk"

# インスタンス
audio = pyaudio.PyAudio()
features = features.Features()
eval_model = eval_model.EvalModel()

# グローバル変数
GENRE_LIST = ["1_mizuoto1", "2_tearai", "3_handwash", "4_kao", "5_voice", "6_muon", "9_ugai_only" ]
pred_total  = []
frames = []
num = 1
pred_mizu_total = 0

# プログラム開始時にSVMにより分類器を作成しておく
x, y = features.read_ceps(GENRE_LIST, DATA_DIR )
svc = LinearSVC(C=1.0)
x,y = resample(x,y,n_samples=len(y))
svc.fit(x[:400],y[:400])
#prediction = svc.predict(x[80:])

def callback(in_data, frame_count, time_info, status):
    """
    非同期処理を行う
    """
    global num
    global pred_total
    global pred_mizu_total

    # 取得した生活音のwavファイルを作成する
    os.chdir(STREAM_DIR)
    frames.append(in_data)
    WAVE_OUTPUT_FILENAME = "file%d.wav" %num
    CEPS_OUTPUT_FILENAME = "file%d.ceps.npy" %num
    try:
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
    except:
        print "Error"

    # wavファイルから特徴量を抽出し、あらかじめ作成した分類器にかける
    features.create_ceps(WAVE_OUTPUT_FILENAME)
    x = features.read_ceps2(CEPS_OUTPUT_FILENAME)
    pred = svc.predict(x)
    print_pred(pred)

    # 分類結果を記録する
    pred_total.append("%d" %pred)
    pred_mizu_total = pred_total.count("0") + pred_total.count("1") + pred_total.count("2") + pred_total.count("4")
    print(pred_total)
    print(pred_mizu_total)

    num += 1
    del frames[:]
    return(None, pyaudio.paContinue)

def wavplay(dir, wavfile):
    """
    あらかじめ作成したwavファイルを再生する
    """

    # 再生用のコールバック関数を定義しておく
    def wavcallback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # WAVファイルを再生するためのストリームを作成〜再生〜解放
    os.chdir(dir)
    wf = wave.open(wavfile, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=wavcallback)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

def print_pred(pred):
    """
    分類結果をコンソール出力する
    """
    d = datetime.datetime.today()
    if pred ==0:
        print u'%s時%s分%s秒    %d : 水流音1 ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./水流音１.wav"
        wavplay(CLASS_DIR, wavefile)
    if pred ==1:
        print u'%s時%s分%s秒    %d : 手洗い音 ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./手洗い音.wav"
        wavplay(CLASS_DIR, wavefile)
    if pred ==2:
        print u'%s時%s分%s秒    %d : 石鹸音 ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./石鹸音.wav"
        wavplay(CLASS_DIR, wavefile)
    if pred ==3:
        print u'%s時%s分%s秒    %d : 顔洗い音 ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./顔洗い音.wav"
        wavplay(CLASS_DIR, wavefile)
    if pred ==4:
        print u'%s時%s分%s秒    %d : 声 ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./声.wav"
        wavplay(CLASS_DIR, wavefile)
    if pred ==5:
        print u'%s時%s分%s秒    %d : 無音 ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./無音.wav"
        wavplay(CLASS_DIR, wavefile)
    if pred ==6:
        print u'%s時%s分%s秒    %d : うがい ' % (d.hour, d.minute, d.second, pred)
        wavefile = u"./うがい音.wav"
        wavplay(CLASS_DIR, wavefile)

if __name__ == "__main__":
    """
    初期起動関数
    """
    # 音声の録音を行うためのストリーム作成〜解放(実際の録音はcallback関数で行う)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=2,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    print (u"")
    print ("[0:水流音1，1:手洗い音，2:石鹸音，3:顔洗い音，4:声，5:無音，6:うがい]")
    print ("recording...")
    stream.start_stream()
    time.sleep(RECORD_SECONDS)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 水を一定以上出し続けた場合、警告を行う
    if pred_mizu_total >= 5:
        #wavefile = u"./01_水道水つかいすぎだよ….wav"
        wavplay(TALK_DIR, wavefile)
