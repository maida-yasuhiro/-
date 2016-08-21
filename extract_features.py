# -*- coding: utf-8 -*-

u"""Header Info
  音楽ファイルから特徴量を抽出する
"""

import features
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

genre_list = ["1_mizuoto1", "1_mizuoto2", "2_tearai", "3_handwash", "4_kao", "5_voice", "6_muon", "9_ugai_only" ]

if __name__ == "__main__":
    """
    初期起動関数
    """
    features = features.Features()
    for num in range(1,17):
        fn = "./%d.wav" %num
        features.create_ceps(fn)
