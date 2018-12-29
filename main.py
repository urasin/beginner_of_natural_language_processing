import os
import time
import tqdm
import numpy as np
import pandas as pd
import MeCab

# 単語リストを半角空白で結合された1行テキストに変換する関数
def list2line(word_list):
  line = ''
  for word in words_list:
    line += word
    line += " "
  return line[:-1] # [:-1]で末尾の文字れるを除ける

# 分かち書き用のクラス定義(tokenを取得)
class Wakati:
  def __init__(self, text=""):
    self.text = text
    self.targets = ["名詞", "動詞", "形容詞"]
    self.stopwords = ["する", "もの", "れる", "ない", "られる", "こと", "ある", "ため", "これ", "いる", "なる", "よる", "よう"]
    
  # 分かち書きを行うメソッド(外へのInterface)
  def tokenize(self):
      words = self. get_word_from_text()
      tokens = self.exclude_stopped_words(words)
      return tokens

  def exclude_stopped_words(self, words):
    return [ word for word in words if word not in self.stopwords ]

  # 形態素解析から対象となる品詞(self.targets)の単語リストを返す関数
  def get_word_from_text(self):
    df = self.convert_text_to_dfw()
    words = []
    # https://note.nkmk.me/python-pandas-dataframe-for-iteration/
    # row[0] => index, row[1] => column Series type like (dict{column_name: value})
    for row in df.iterrows():
      if row[1]['POS'] not in self.targets:
        continue
      if row[1]["STEM"] == "*":
        continue
      words.append(row[1]["STEM"])
    return words

  # テキストの形態素解析結果をDataFrame(dfm)で返す関数
  # DataFrameだとなにが嬉しいか調査したい => index(左一列), colmun(index以外の各列)の表形式でデーターを操作できるのがうれしい？
  # 使い方: https://qiita.com/osk_kamui/items/0a164ec002ff6d8798ca
  # <class 'pandas.core.frame.DataFrame'>
  # http://dlrecord.hatenablog.com/entry/2017/10/30/182708
  def convert_text_to_dfw(self):
    # 分かち書きらしい
    t = MeCab.Tagger("Owakachi")
    # Workaround https://qiita.com/piruty/items/ce218090eae53b775b79
    t.parse("")
    text = "私の好きな果物はバナナです。"
    node = t.parseToNode(text)
    surface_list = []
    part_of_speech_list=[]
    stem_list = []
    while node:
      features = node.feature.split(',')
      # 品詞
      part_of_speech = features[0]
      part_of_speech_list.append(part_of_speech)
      # stem関数? 幹
      # https://bellcurve.jp/statistics/course/5228.htmle
      # '私'とか'の'とか'。', '*'とか入る
      stem = features[6]
      stem_list.append(stem)
      surface = node.surface
      surface_list.append(surface)
      node = node.next

    df = pd.DataFrame()
    df["SURFACE"] = surface_list[1:-1]  # [1:-1]で先頭と丸美を取り除く、return list
    df["POS"] = part_of_speech_list[1:-1]
    df["STEM"] = stem_list[1:-1]
    return df

Wakati().tokenize()
