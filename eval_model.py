# -*- coding: utf-8 -*-

u"""Header Info
  分類器の評価を行う
"""

from matplotlib import pylab

class EvalModel:
    u"""
    作成した分類器の評価を行う際の,
    必要な処理を行う
    """
    def __init__(self):
        u"""
        コンストラクタ
        """
        self.name = ""

    def normalisation(self, cm):
        u"""
        混合行列の正規化を行い、値を0~1の範囲に収める
        """
        new_cm = []
        for line in cm:
            sum_val = sum(line)
            new_array = [float(num)/float(sum_val) for num in line]
            new_cm.append(new_array)
        return new_cm

    def plot_confusion_matrix(self, cm, genre_list, title):
        u"""
        混合行列をプロットする
        """
        pylab.clf()
        pylab.matshow(cm, fignum=False, cmap='Blues', vmin=0, vmax=1.0)
        ax = pylab.axes()
        ax.set_xticks(range(len(genre_list)))
        ax.set_xticklabels(genre_list)
        ax.xaxis.set_ticks_position("bottom")
        ax.set_yticks(range(len(genre_list)))
        ax.set_yticklabels(genre_list)
        pylab.title(title)
        pylab.colorbar()
        pylab.grid(False)
        pylab.xlabel('Predicted class')
        pylab.ylabel('True class')
        pylab.grid(False)
        pylab.show()

