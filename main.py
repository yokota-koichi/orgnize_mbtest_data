import pandas as pd
import numpy as np
import os

def data_pick(path):
    # FFTのtxtファイル読み込み．最初の14行と最後の1行は読み込まない
    df = pd.read_csv(filepath_or_buffer= path, skiprows=16, skipfooter=1)
    print(df)

root_dir = 'data/'

for folder in os.listdir(root_dir):
    # MB_xxx以外のフォルダがディレクトリに存在する場合は除外
    if not ('MB' in folder):
        continue
    print(folder)

files = os.listdir(root_dir)

for file in files:
    path  = root_dir + file
    data_pick(path)
    break


