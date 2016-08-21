# -*- coding: utf-8 -*-

u"""Header Info
  対話型洗面台の音声認識部分の分類器を作成する
                 - 学習モデル : SVM
                 - 特徴量 : MFCC (13次元)
                 - データ分割 : ホールドアウト法
                 - 評価方法 : 混合行列、ROC曲線
"""

# 自作ライブラリ
import features
import eval_model

# 外部ライブラリ
import scipy
import numpy as np
import glob
from matplotlib.pyplot import specgram
from scipy.io import wavfile
import os
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.utils import resample
from matplotlib import pylab
from matplotlib.pylab import clf

genre_list = ["1_mizuoto1", "2_tearai", "3_handwash", "4_kao", "5_voice", "6_muon", "9_ugai_only" ]
#genre_list = ["4_kao"]
cur_dir = os.getcwd()
print (cur_dir)
#DATA_DIR = cur_dir + "/musicdata_client"
DATA_DIR = cur_dir + "/seikatsuon"
#DATA_DIR = cur_dir + "/data"
print (DATA_DIR)
if __name__ == "__main__":
    """
    初期起動関数
    """
    features = features.Features()
#    x, y = features.read_fft(genre_list)
    x, y = features.read_ceps(genre_list, DATA_DIR)
    # データをシャッフルし、17~24番目までをテストデータ、1~16番目を教師データとした
#    print x
#    print y
    svc = LinearSVC(C=1.0)
    x,y = resample(x,y,n_samples=len(y))
    # 訓練データを使ってフィッティング
    a = svc.fit(x[:400],y[:400])
#    a = svc.fit(x[:80],y[:80])
    print (a)
    # テストデータ
#    prediction = svc.predict(x[220:])
    prediction = svc.predict(x[400:])
    print(prediction)

#    cm = confusion_matrix(y[220:], prediction)
    cm = confusion_matrix(y[400:], prediction)
#    print(cm)
    eval_model = eval_model.EvalModel()
    cm = eval_model.normalisation(cm)
    print(cm[0])
    print(cm[1])
    print(cm[2])
    print(cm[3])
    print(cm[4])
    print(cm[5])
    print(cm[6])
#    print(cm[7])
#    print(cm[8])
#    print(cm[7])
    #print(cm)
#    title = "FFT"
    title = "MFCC"
    eval_model.plot_confusion_matrix(cm, genre_list, title)

