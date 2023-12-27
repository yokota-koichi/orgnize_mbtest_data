import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker
from scipy.signal import find_peaks
from matplotlib.backends.backend_pdf import PdfPages

# FFTとボード線図とハンマリング試験結果のデータを分別する関数
def data_split():
    root_dir = 'data'
    spec_path_folder_list = []
    transfunc_path_folder_list = []
    hammer_path_folder_list = []

    # data内のフォルダを1つずつ検索
    for folder in os.listdir(root_dir):
        # root_dir内のフォルダ（MB_xxx）のパスを一時的に格納する．
        tmp = root_dir + '/' + folder

        # MB_xxx以外のフォルダがディレクトリに存在する，または，フォルダ内が空の場合除外
        if ((('MB')  in folder) and (os.listdir(tmp) != [])):
            # 伝達関数測定のデータを格納
            if '13' in folder:
                transfunc_path_folder_list.append(tmp)
            # ハンマリングの試験結果を格納
            elif '16' in folder:
                hammer_path_folder_list.append(tmp)
            # FFTのデータを格納
            else:
            # FFTのデータが存在するフォルダだけのリストを作成
                spec_path_folder_list.append(tmp)

    return spec_path_folder_list, transfunc_path_folder_list, hammer_path_folder_list

def set_limit():
    return 0

def find_peaks(x,y,n_freq):
    idx_1 = np.argmin(np.abs(np.array(x)-n_freq))
    idx_2 = np.argmin(np.abs(np.array(x)-n_freq*2))
    idx_3 = np.argmin(np.abs(np.array(x)-n_freq*3))

    peak_rigid_idx = np.argmax(y[:idx_1-10])
    peaks_elastic = np.max([np.max(y[idx_1+20:idx_2-20]),np.max(y[idx_2+20:idx_3-20]),np.max(y[idx_3+20:])])
    peak_elastic_idx = list(y).index(peaks_elastic)

    return [peak_rigid_idx, peak_elastic_idx]



def make_spec_graph(folder_list, pdf):
    for folder_path in folder_list:
        # txtファイルのフルパスを取得
        files = glob.glob(folder_path + "/*")
        fig = plt.figure(figsize=(8,5))
        ax = []
        for j in range(len(files)):
            ax.append(fig.add_subplot(2,2,j+1))

        for j in range(len(files)):
            # FFTのtxtファイル読み込み．最初の14行と最後の1行は読み込まない
            df = pd.read_csv(filepath_or_buffer= files[j], skiprows=16, skipfooter=1, encoding='shift-jis', engine='python')

            x = df.iloc[:,0]
            y = df.iloc[:,1]
            peaks = find_peaks(x,y,562.5)
            ax[j].set_ylim(-120,0)
            ax[j].set_xlabel('Frequency [Hz]')
            ax[j].set_ylabel('Mag [dBV]')
            ax[j].grid(which='major',color='gray',linestyle='-',linewidth=0.1)
            ax[j].grid(which='minor',color='gray',linestyle='--',linewidth=0.1)
            ax[j].scatter(x[peaks], y[peaks], color= 'red', s=5, marker="x")
            for peak in peaks:
                ax[j].text(x[peak]+10, y[peak]+5, str(round(y[peak],1)))
            ax[j].plot(x,y, linewidth=0.5)
            # ax[j].legend()
        fig.suptitle("yes")
        plt.tight_layout()

        pdf.savefig()
        """
        # 評価項目ごとにpdfを分けたいならこのコメントブロック内のコードを有効にする．
        # save_dir = 'fig/' + folder_path.split('/')[1]
        # save_path = save_dir + '/' + folder_path.split('/')[1] +'.pdf'
        # os.makedirs(save_dir, exist_ok=True)
        # plt.savefig(save_path)
        """
        plt.clf()
        plt.close()

def make_transfunc_graph(folder_list, pdf):


    cnt = 0
    for folder_path in folder_list:
        files = glob.glob(folder_path + "/*")
        if cnt%3 == 0:
            fig = plt.figure(figsize=(10,5))
            ax = []
            for j in range(6):
                ax.append(fig.add_subplot(2,3,j+1))


        # 位相のtxtファイル読み込み．最初の19行は読み込まない
        df1 = pd.read_csv(filepath_or_buffer= files[0], skiprows=19, skipfooter=0, encoding='shift-jis', engine='python')
        # ゲインのtxtファイル読み込み．
        df2 = pd.read_csv(filepath_or_buffer= files[2], skiprows=19, skipfooter=0, encoding='shift-jis', engine='python')
        x1 = df1.iloc[:,0]
        y1 = df1.iloc[:,1]
        x2 = df2.iloc[:,0]
        y2 = df2.iloc[:,1]
        ax[cnt].set_ylim(-200,200)
        ax[cnt+3].set_ylim(-100,100)
        ax[cnt].set_xlabel('Frequency [Hz]')
        ax[cnt].set_ylabel('Mag [dBV]')
        ax[cnt+3].set_xlabel('Frequency [Hz]')
        ax[cnt+3].set_ylabel('Phase [deg]')
        ax[cnt].set_xscale("log")
        ax[cnt+3].set_xscale("log")
        ax[cnt].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax[cnt+3].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax[cnt].grid(which='major',color='gray',linestyle='-',linewidth=0.1)
        ax[cnt].grid(which='minor',color='gray',linestyle='--',linewidth=0.1)
        ax[cnt+3].grid(which='major',color='gray',linestyle='-',linewidth=0.1)
        ax[cnt+3].grid(which='minor',color='gray',linestyle='--',linewidth=0.1)
        ax[cnt].plot(x1,y1, linewidth=0.8)
        ax[cnt+3].plot(x2,y2, linewidth=0.8)
        # ax[j].legend()


        if cnt%3 == 2:

            fig.suptitle("yes")
            plt.tight_layout()

            pdf.savefig()

            plt.clf()
            plt.close()
            cnt = 0

        else:
            cnt += 1

def make_all_graph(spec_path_folder_list, transfunc_path_folder_list, hammer_path_folder_list):
    pdf_path = "graph.pdf"
    graph_pdf = PdfPages(pdf_path)
    # make_spec_graph(spec_path_folder_list, graph_pdf)

    make_transfunc_graph(transfunc_path_folder_list, graph_pdf)

    graph_pdf.close()

spec, transfunc, hammer = data_split()
make_all_graph(spec, transfunc, hammer)







