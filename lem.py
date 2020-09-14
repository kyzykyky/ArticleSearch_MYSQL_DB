import re

path = 'D:/Documents/NotMyCodes/Python/Morfik/zhalgau'


def bolu(t):
    delim = re.compile(u'\n')
    sent = delim.split(t)
    return sent


def jalgau(soz):
    tgsoz = ''
    # soz = input("Soz: ")
    wl = len(soz)
    # print("wl = ", wl)

    t = []

    if wl > 14:
        f = open(path + '/13zh.txt', 'r', encoding='utf8')
        # print('w>14')

        buf = ''

        for i in range(13, 0, -1):
            if i == 13:
                f = open(path + "/13zh.txt", 'r', encoding="utf-8")
                print("13 is open")
            if i == 12:
                f = open(path + "/12zh.txt", 'r', encoding="utf-8")
                print("12 is open")
            if i == 11:
                f = open(path + "/11zh.txt", 'r', encoding="utf-8")
                print("11 is open")
            if i == 10:
                f = open(path + "/10zh.txt", 'r', encoding="utf-8")
                print("10 is open")
            if i == 9:
                f = open(path + "/9zh.txt", 'r', encoding="utf-8")
                print("9 is open")
            if i == 8:
                f = open(path + "/8zh.txt", 'r', encoding="utf-8")
                print("8 is open")
            if i == 7:
                f = open(path + "/7zh.txt", 'r', encoding="utf-8")
                print("7 is open")
            if i == 6:
                f = open(path + "/6zh.txt", 'r', encoding="utf-8")
                print("6 is open")
            if i == 5:
                f = open(path + "/5zh.txt", 'r', encoding="utf-8")
                print("5 is open")
            if i == 4:
                f = open(path + "/4zh.txt", 'r', encoding="utf-8")
                print("4 is open")
            if i == 3:
                f = open(path + "/3zh.txt", 'r', encoding="utf-8")
                print("3 is open")
            if i == 2:
                f = open(path + "/2zh.txt", 'r', encoding="utf-8")
                print("2 is open")
            if i == 1:
                f = open(path + "/1zh.txt", 'r', encoding="utf-8")
                print("1 is open")
            if i == 0:
                f = open(path + "/0zh.txt", 'r', encoding="utf-8")
                print("0 is open")

            sj = soz[wl - i:]
            buf = f.read()
            arrj = bolu(buf)
            t = []

            for j in arrj:
                if j == sj and j != '':
                    t.append(soz[:wl - len(j)])
                    # y = soz[:wl-len(j)]
            # break
        f.close()

    # -----------------------------------------------------------------------------------------------------------------------

    if wl <= 14:
        f = open(path + '/13zh.txt', 'r', encoding='utf8')
        # print('w<=14')

        t = []
        for i in range(wl - 2, 0, -1):
            if i == 13:
                f = open(path + "/13zh.txt", 'r', encoding="utf-8")
            if i == 12:
                f = open(path + "/12zh.txt", 'r', encoding="utf-8")
            if i == 11:
                f = open(path + "/11zh.txt", 'r', encoding="utf-8")
            if i == 10:
                f = open(path + "/10zh.txt", 'r', encoding="utf-8")
            if i == 9:
                f = open(path + "/9zh.txt", 'r', encoding="utf-8")
            if i == 8:
                f = open(path + "/8zh.txt", 'r', encoding="utf-8")
            if i == 7:
                f = open(path + "/7zh.txt", 'r', encoding="utf-8")
            if i == 6:
                f = open(path + "/6zh.txt", 'r', encoding="utf-8")
            if i == 5:
                f = open(path + "/5zh.txt", 'r', encoding="utf-8")
            if i == 4:
                f = open(path + "/4zh.txt", 'r', encoding="utf-8")
            if i == 3:
                f = open(path + "/3zh.txt", 'r', encoding="utf-8")
            if i == 2:
                f = open(path + "/2zh.txt", 'r', encoding="utf-8")
            if i == 1:
                f = open(path + "/1zh.txt", 'r', encoding="utf-8")
            if i == 0:
                f = open(path + "/0zh.txt", 'r', encoding="utf-8")
            sj = soz[wl - i:]
            buf = f.read()
            arrj = bolu(buf)

            for j in arrj:
                if j == sj and j != '':
                    t.append(soz[:wl - len(j)])
                    # y = soz[:wl-len(j)]
            # break
        f.close()
    # print('buf: ', t[0])
    return t[0]
    # print('y: ', y)

# -----------------------------------------------------------------------------------------------------------------------


# coz = input("Soz: ")
# lemma = jalgau(coz)
# print(lemma)
