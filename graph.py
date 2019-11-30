from matplotlib import pyplot as plt
import Adafruit_DHT

def main():
    plt.figure()
    xlim = [0,50]
    x, y_hum, y_temp = [], [], []
    sensor = Adafruit_DHT.DHT22
    pin = 23
   
    while True:
        hum, temp = Adafruit_DHT.read_retry(sensor, pin)
        hum = round(hum, 1)
        temp = round(temp, 1)

        plt.cla()

        y_hum.append(hum)
        y_temp.append(temp)
        x.append(len(y_hum))

        if len(x) > 50:
            xlim[0] += 1
            xlim[1] += 1

        plt.plot(x, y_hum, label='humidity')
        plt.plot(x, y_temp, label='temperature')

        plt.legend()
        plt.ylim([0, 100])
        plt.xlim(xlim[0], xlim[1])
        plt.pause(0.25)


if __name__ == '__main__':
    main()