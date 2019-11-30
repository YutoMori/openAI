#app.py
from flask import Flask, render_template
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

import os
import glob

app = Flask(__name__)


@app.route("/plot/<func>")
def plot_graph(func='01'):
    fig = Figure()
    ax = fig.add_subplot(111)
    df = pd.read_csv('all.csv')
    
    df = df[df['id'] == int(func)]
    ax.plot(df['hum'], color='C0', label='humidity')
    ax.set_ylim([0,100])
    ax.set_ylabel('humidity')
    ax1 = ax.twinx()
    ax1.plot(df['temp'], color='C1', label='temperature')
    ax1.set_ylim([0, 40])
    ax1.set_ylabel('temperature')

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
        list_df.append(pd.read_csv(file_name))
    df = pd.concat(list_df, sort=False)
    df.to_csv('./all.csv')
    print("merge csv")
    return render_template("index.html", img_data=None)

if __name__ == "__main__":
    app.run(debug=True)