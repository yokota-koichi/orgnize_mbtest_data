import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# FFTとボード線図とハンマリング試験結果のデータを分別する関数
def data_split():
    root_dir = 'data'
    fft_path_folder_list = []
    boad_path_folder_list = []
    hammer_path_folder_list = []

    # data内のフォルダを1つずつ検索
    for folder in os.listdir(root_dir):
        # root_dir内のフォルダ（MB_xxx）のパスを一時的に格納する．
        tmp = root_dir + '/' + folder

        # MB_xxx以外のフォルダがディレクトリに存在する，または，フォルダ内が空の場合除外
        if ((('MB')  in folder) and (os.listdir(tmp) != [])):
            # 伝達関数測定のデータを格納
            if '13' in folder:
                boad_path_folder_list.append(tmp)
            # ハンマリングの試験結果を格納
            elif '16' in folder:
                hammer_path_folder_list.append(tmp)
            # FFTのデータを格納
            else:
            # FFTのデータが存在するフォルダだけのリストを作成
                fft_path_folder_list.append(tmp)

    return fft_path_folder_list, boad_path_folder_list, hammer_path_folder_list




def make_graph(folder_list):
    for folder_path in folder_list:
        file = glob.glob(folder_path + "/*")
        fig = plt.figure()
        ax = []
        for j in range(len(file)):
            ax.append(fig.add_subplot(2,2,j+1))

        for j in range(len(file)):
            # FFTのtxtファイル読み込み．最初の14行と最後の1行は読み込まない
            df = pd.read_csv(filepath_or_buffer= file[j], skiprows=16, skipfooter=1, encoding='shift-jis', engine='python')

            x = df.iloc[:,0]
            y = df.iloc[:,1]
            peaks, _ = find_peaks(y, prominence=15)

            ax[j].set_ylim(-120,0)
            ax[j].scatter(x[peaks], y[peaks], color= 'red')
            ax[j].plot(x,y, linewidth=0.8)

        save_dir = 'fig/' + folder_path.split('/')[1]
        save_path = save_dir + '/' + folder_path.split('/')[1] +'.pdf'
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(save_path)
        plt.clf()
        plt.close()



tmp, _, _ =data_split()
make_graph(tmp)






