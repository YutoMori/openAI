#app.py
from flask import Flask, render_template
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import pandas as pd
import datetime

import os
import glob

app = Flask(__name__)


@app.route("/plot/<func>")
def plot_graph(func='01'):
    fig = Figure()
    ax = fig.add_subplot(111)
    df = pd.read_csv('all.csv', usecols=['id', 'ut', 'temp', 'hum'])

    # ut(時刻)を基に昇順ソートする
    df.sort_values('ut', inplace=True)

    df = df[df['id'] == int(func)]
    print(df)
    ax.plot(df['ut'], df['hum'], color='C0', label='humidity')
    ax.set_ylim([0,100])
    ax.set_ylabel('humidity')
    ax1 = ax.twinx()
    
    ax1.set_ylim([0, 40])
    ax1.set_ylabel('temperature')
    ax1.plot(df['ut'], df['temp'], color='C1', label='temperature')
    
    fig.autofmt_xdate()

    fig.legend()
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
    
    # python の list型 から pandas の DataFrame型 に変更
    df = pd.concat(list_df, sort=False)
    df.to_csv('./all.csv')

    df['ut'] = df['ut'].astype(int)
    df['ut'] = pd.to_datetime(df['ut'], unit="s")
    df['ut'] += pd.tseries.offsets.Hour(9) # 日本の時刻に合わせる
    df.to_csv('./all_datetime.csv')
    print("merge csv")
    return render_template("index.html", img_data=None)

if __name__ == "__main__":
    app.run(debug=True)