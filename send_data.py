import Adafruit_DHT
import pandas as pd
import time

sensor = Adafruit_DHT.DHT22
pin = 23
hum, temp = Adafruit_DHT.read_retry(sensor, pin)
hum = round(hum, 1)
temp = round(temp, 1)
df = pd.DataFrame([['01', time.time(), temp, hum]], columns=['id', 'ut', 'temp', 'hum'])
time.sleep(1)

while True:
    try:
        hum, temp = Adafruit_DHT.read_retry(sensor, pin)
        hum = round(hum, 1)
        temp = round(temp, 1)
        new_df = pd.DataFrame([['01', time.time(), temp, hum]], columns=['id', 'ut', 'temp', 'hum'])
        df = df.append(new_df)

        if hum is not None and temp is not None:
            print(new_df)
        else:
            print('Failed to get reading. Try again!')
            exit()
        
        time.sleep(1)

    except KeyboardInterrupt:
        print("end")
        df.to_csv("out_test.csv")
        exit()
