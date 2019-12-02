import Adafruit_DHT
import pandas as pd
import time

# センサ情報
sensor = Adafruit_DHT.DHT22
pin = 23

# 空のDataFrameを作成
df = pd.DataFrame()

while True:
    try:
        # 温度と湿度を受け取る
        hum, temp = Adafruit_DHT.read_retry(sensor, pin)
        hum = round(hum, 1)
        temp = round(temp, 1)

        user_id = '01' # PCのユーザIDを記述
        
        # ユーザid, 現在のUnixTime, 気温, 湿度を追加
        new_df = pd.DataFrame([[user_id, time.time(), temp, hum]], columns=['id', 'ut', 'temp', 'hum'])
        df = df.append(new_df)

        if hum is not None and temp is not None:
            print(new_df)
        else:
            print('Failed to get reading. Try again!')
            exit()
        
        time.sleep(1)

    except KeyboardInterrupt: # ctrl+c で中止したとき
        print("end")
        csv_name = "output" + user_id + "_" + str(int(time.time())) + ".csv"
        df.to_csv(csv_name)
        exit()
