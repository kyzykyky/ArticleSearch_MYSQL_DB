import re
# import nltk

path = 'zhalgau'


def sozgebolu(text):
    result = re.findall(r'\w+', str.lower(text))
    return result


# ------------------------------------------------------------------------------------------

def bolu(t):
    delim = re.compile(u'\n')
    sent = delim.split(t)
    return sent


def openfile(i):
    f = '☺'
    if i == 13:
        f = open(path + "/13zh.txt", 'r', encoding="utf-8")
    if i == 12:
        f = open(path + "/13zh.txt", 'r', encoding="utf-8")
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
    return f


# функция который возвращает основу слова
def negiz(soz):
    tgsoz = ''
    wl = len(soz)
    t = []

    if wl > 14:
        f = open(path + '/13zh.txt', 'r', encoding='utf8')


        for i in range(13, 0, -1):
            f = openfile(i)
            sj = soz[wl - i:]
            buf = f.read()
            arrj = bolu(buf)

            for j in arrj:
                if j == sj:
                    t.append(soz[:wl - len(j)])
                if j == '' or sj == '':
                    t.append(soz[:wl])
        f.close()

    if wl <= 14 and wl > 2:
        f = open(path + '/13zh.txt', 'r', encoding='utf8')

        for i in range(wl - 2, -1, -1):
            f = openfile(i)
            sj = soz[wl - i:]
            buf = f.read()
            arrj = bolu(buf)

            for j in arrj:
                if j == sj:
                    t.append(soz[:wl - len(j)])
                if j == '' or sj == '':
                    t.append(soz[:wl])
        f.close()

    if wl == 2 or wl == 1:
        return soz

    return t[0]


# =================================================================================================

# fl1 = open("7tarihitulga.txt", 'r', encoding="utf-8")
# txt1 = fl1.read()
#
# # разбивка текста по словам
# soz = sozgebolu(txt1)
#
# # удалить стоп слова
# fl2 = open("stopwords.txt", 'r', encoding="utf-8")
# txt2 = fl2.read()
# sw = sozgebolu(txt2)
#
# for k in range(1, len(soz), 1):
#     for i in soz:
#         for j in sw:
#             if i == j:
#                 soz.remove(j)
#
#             # вывод основы слова
# lemmas = []
# h = 0
# while h < len(soz):
#     lemma = negiz(soz[h])
#     lemmas.append(lemma)
#     h += 1
#
# print(lemmas)
