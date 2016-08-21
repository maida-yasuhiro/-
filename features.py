# -*- coding: utf-8 -*-

u"""Header Info
  音楽ファイルから特徴量を抽出する
"""

from scikits.talkbox.features import mfcc
import scipy
from scipy import io
from scipy.io import wavfile
import glob
import numpy as np
import os

cur_dir = os.getcwd()
#os.chdir(cur_dir + "/senmendai1/9_ugai_only")
GENRE_DIR = cur_dir
#BASE_DIR = cur_dir + "/musicdata"
#GENRE_DIR = cur_dir + "/musicdata"

class Features:
    u"""
    音楽ファイルから特徴量の抽出を行う際の,
    必要な処理を行う
    """
    def __init__(self):
        u"""
        コンストラクタ
        """
        self.name = ""

    def write_ceps(self, ceps, fn):
        u"""
        mfccの結果をキャッシュとして保存する
        """
        base_fn,ext = os.path.splitext(fn)
        data_fn = base_fn + ".ceps"
        np.save(data_fn,ceps)
        #print("Written %s" % data_fn)

    def create_ceps(self, fn):
        u"""
        音楽ファイル(.wav)に対してMFCCを求め、
        キャッシュファイル(.npy)を作成し、セーブする
        """
        sample_rate,X = io.wavfile.read(fn)
        # ceps:fnの各フレームに対する13個の係数が格納されている
        # Nanを無視する
        ceps,mspec,spec = mfcc(X)
        isNan = False
        for num in ceps:
            if np.isnan(num[1]):
                isNan = True
        if isNan == False:
            self.write_ceps(ceps,fn)

    def read_ceps(self, name_list, base_dir):
        u"""
        mfccのキャッシュデータを読み込む
        引数 name_list : ディレクトリ名のリスト
        """
        X,y = [],[]
        for label,name in enumerate(name_list):
            for fn in glob.glob(os.path.join(base_dir,name,"*.npy")):
                ceps = np.load(fn)
                num_ceps = len(ceps)
                X.append(np.mean(
                    ceps[int(num_ceps*2/10):int(num_ceps*9/10)],axis=0))
                y.append(label)

        return np.array(X),np.array(y)

    def read_ceps2(self, fn):
        u"""
        mfccのキャッシュデータを読み込む
        """
        X = []
        #print (fn)
        ceps = np.load(fn)
        num_ceps = len(ceps)
        X.append(np.mean(
            ceps[int(num_ceps*2/10):int(num_ceps*9/10)],axis=0))

        return np.array(X)

