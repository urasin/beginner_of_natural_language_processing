import re
import os
import time
import tqdm
import codecs
import pandas as pd

from libs.wakati import Wakati


class TokenData:
  """分かち書きした結果を出力するためのクラス."""

  def __init__(self, data_dir_path):
    self.data_dir_path = data_dir_path

  def output_csv(self, path="./dist/tokenized_data.csv"):
    """テキストを分かち書きした結果をcsvファイルで出力する"""
    df_tokenized = self._get_df_tokenized()
    print(df_tokenized.head())
    df_tokenized.to_csv(path, encoding="utf8", index=False)
  
  def _get_df_tokenized(self):
    """ ファイルを分かち書きした結果をDataFrameで返す"""
    filenames = self._list_filenames_data_dir()
    filepaths = self._list_filepaths_data_dir(filenames)
    texts = [self._open_text(filepath) for filepath in tqdm.tqdm(filepaths)]
    toknenized_texts = [" ".join(Wakati(text).tokenize()) for text in texts]
    df_tokenized = pd.DataFrame()
    df_tokenized["filename"] = filenames
    df_tokenized["token"] = toknenized_texts
    return df_tokenized
  
  def _list_filepaths_data_dir(self, filenames):
    """ data_dir_path直下の.txtのファイルパス一覧を返す"""
    return [os.path.join(self.data_dir_path, filename) for filename in filenames]

  def _list_filenames_data_dir(self):
    """ data_dir_path直下の.txtのファイル名一覧を返す"""
    return [filename for filename in os.listdir(self.data_dir_path) if ".txt" in filename]
  
  def _open_text(self, filepath):
    """テキストファイルからテキストを抽出して返す"""
    with codecs.open(filepath, "r", "utf8", "ignore") as f:
      return f.read()

if __name__ == "__main__":
  data_dir_path = "./data/"
  td = TokenData(data_dir_path)
  td.output_csv()

