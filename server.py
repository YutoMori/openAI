#app.py
from flask import Flask, render_template
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import pandas as pd

import os
import glob

app = Flask(__name__)


@app.route("/plot/<func>")
def plot_graph(func='01'):
    fig = Figure()
    ax1 = fig.add_subplot(111)
    # all.csv の 'id', 'ut', 'temp', 'hum' をDataFrame型に変換
    df = pd.read_csv('all.csv', usecols=['id', 'ut', 'temp', 'hum'])

    # ut(時刻)を基に昇順ソートする
    df.sort_values('ut', inplace=True)

    # htmlで選択したuser_idのデータを抽出する
    df = df[df['id'] == int(func)]
    print(df)

    # グラフに湿度をプロット
    ax1.plot(df['ut'], df['hum'], color='C0', label='humidity')
    ax1.set_ylim([0,100])
    ax1.set_ylabel('humidity')

    # グラフに温度をプロット
    ax2 = ax1.twinx()  # ax1(湿度)と同じx軸を使う
    ax2.set_ylim([0, 40])
    ax2.set_ylabel('temperature')
    ax2.plot(df['ut'], df['temp'], color='C1', label='temperature')
    
    fig.autofmt_xdate()
    
    # グラフ軸の設定
    fig.legend()

    # 作成したグラフを画像に変換し、htmlで表示させる
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    img_data = urllib.parse.quote(png_output.getvalue())
    return img_data


@app.route("/")
def index():
    # フォルダ内のパスを取得
    DATA_PATH = "./csv/"
    ALL_files = glob.glob('{}*.csv'.format(DATA_PATH))
    
    # フォルダ内の全csvをマージ
    list_df = []
    for file_name in ALL_files:
        list_df.append(pd.read_csv(file_name, usecols=['id', 'ut', 'temp', 'hum']))
    
    # python の list型 から pandas の DataFrame型 に変換
    df = pd.concat(list_df, sort=False)
    print("merge csv")
    df.to_csv('./all.csv')

    # Unixtime を pandas の datetime型に変換
    df['ut'] = df['ut'].astype(int)
    df['ut'] = pd.to_datetime(df['ut'], unit="s")
    df['ut'] += pd.tseries.offsets.Hour(9) # 日本の時刻に合わせる
    df.to_csv('./all_datetime.csv')
    
    return render_template("index.html", img_data=None)

if __name__ == "__main__":
    app.run(debug=True)