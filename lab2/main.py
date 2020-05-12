# Вариант 2
# Протарифицировать абонента с IP-адресом 217.15.20.194
# с коэффициентом k: 1руб/Мб, первая 1000Мб бесплатно

import os
import math
import matplotlib.pyplot as plt

import datetime

def get_time(i):
    hour=int(i[1][:2])
    min=int(i[1][3:5])
    sec=int(i[1][6:8])
    return (datetime.time(hour,min,sec))


def tarif(ip):
    os.system("nfdump -r nfcapd.202002251200 >> text.txt")
    f = open('text.txt', 'r', encoding='utf-8')
    f.readline()
    data = []
    q = f.readlines()
    [data.append(i.split()) for i in q]
    data = data[:-4]
    f.close()
    xy=[]
    traf=0.0

    for i in data:
        if i[5][:len(ip)]==ip or i[7][:len(ip)]==ip:
            if i[-2]=='M':
                traf+=float(i[-3])
                xy.append([float(i[-3]),get_time(i)])
            else:
                traf+=(float(i[-2])/1024)/1024
                xy.append([((float(i[-2])/1024)/1024), get_time(i)])

    if traf<1000.0:
        traf=traf-0.9765625
    traf = math.ceil(traf)
    return [traf,xy]



def plot(xy):
    xy=sorted(xy, key=lambda x: x[1])
    x=[]
    y=[]
    for i in xy:
        y.append(i[0])
        x.append(str(i[1]))
    ax = plt.axes()
    ax.set_ylabel("Mb", fontsize=14)
    ax.set_xlabel("Time", fontsize=14)
    ax.plot(x, y)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    plt.savefig('plot.png')
    plt.show()

def main():
    f=open('price.txt', 'w',encoding='utf-8')
    price,xy=tarif('217.15.20.194')
    f.write(str(price)+' руб')
    plot(xy)
    f.close()

main()