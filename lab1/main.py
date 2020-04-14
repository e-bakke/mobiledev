# Вариант №2
# Задание:
# Протарифицировать абонента с номером 968247916 с коэффициентом k:
# 3руб/минута исходящие звонки,
# 1руб/минута входящие,
# смс - 1руб/шт

import csv

def parsing(number):
    with open('data.csv', newline='') as csvfile:
        out_calls=[]
        inc_calls=[]
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            if row[1]==number:
                out_calls.append(row)
            if row[2]==number:
                inc_calls.append(row)
        return out_calls,inc_calls


def tariffication(out,inc):
    k = [3, 1, 1]
    calls = [0, 0]
    mes = 0
    for i in out:
        calls[0] += float(i[3])
        mes += float(i[4])
    for i in inc:
        calls[1] += float(i[3])
    x=calls[0]*k[0]+calls[1]*k[1]
    y=mes*k[2]
    return (x,y)

print('Введите номер абонента')
number=str(input())
s=parsing(number)
s=tariffication(s[0],s[1])

f=open('billing.txt', 'w', encoding='utf-8')
f.write(str(s[0])+' - Счет за звонки\n')
f.write(str(s[1])+' - Счет за СМС\n')
f.write(str(s[0]+s[1])+' - Всего')
f.close()