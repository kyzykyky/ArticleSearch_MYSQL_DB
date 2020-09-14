class Numer:
    units = (
        u'нөл',
        u'бір', u'екі', u'үш',
        u'төрт', u'бес', u'алты',
        u'жеті', u'сегіз', u'тоғыз'
    )

    endings = (
        u'дік',
        u'інші', u'нші', u'інші',
        u'інші', u'інші', u'ншы',
        u'нші', u'інші', u'ыншы',
    )
    endings2 = (
        u'ыншы', u'сыншы', u'ыншы',
        u'ыншы', u'інші', u'ыншы',
        u'інші', u'інші', u'ыншы',

        u'інші', u'ыншы'
    )

    tens = (
        u'он', u'жиырма', u'отыз',
        u'қырық', u'елу', u'алпыс',
        u'жетпіс', u'сексен', u'тоқсан'
    )

    hundreds = (
        u'бір жүз', u'екі жүз', u'үш жүз',
        u'төрт жүз', u'бес жүз', u'алты жүз',
        u'жеті жүз', u'сегіз жүз', u'тоғыз жүз'
    )

    orders = (
        u'мың',
        u'миллион',
        u'миллиард',
    )

    orders_ = (
        u'жүз',
        u'мың',
        u'миллион',
        u'миллиард',
    )

    months = (
        u'қаңтар',
        u'ақпан',
        u'наурыз',
        u'сәуір',
        u'мамыр',
        u'маусым',
        u'шілде',
        u'тамыз',
        u'қыркүйек',
        u'қазан',
        u'қараша',
        u'желтоқсан'
    )

    minus = u'минус'

    @staticmethod
    def thousand(rest):
        prev = 0
        name = []
        data = ((Numer.units, 10), (Numer.tens, 100), (Numer.hundreds, 1000))

        for names, x in data:
            cur = int(((rest - prev) % x) * 10 / x)
            prev = rest % x

            if cur == 0:
                continue
            elif x == 10:
                name_ = names[cur]
                if isinstance(name_, tuple):
                    name_ = name_[0]
                name.append(name_)
            else:
                name.append(names[cur - 1])
        return name

    @staticmethod
    def num2text(num, main_units=u'', ord_num=True):
        _orders = (main_units,) + Numer.orders
        if num == 0:
            return ' '.join((Numer.units[0], _orders[0])).strip()  # ноль

        rest = abs(num)
        ord_ = 0
        name = []
        while rest > 0:
            nme = Numer.thousand(rest % 1000)
            if nme or ord_ == 0:
                name.append(_orders[ord_])
            name += nme
            rest = int(rest / 1000)
            ord_ += 1
        if num < 0:
            name.append(Numer.minus)
        name.reverse()
        return ' '.join(name).strip()

    @staticmethod
    def text2numITER(text):  # Not optimal
        for i in range(0, 1000000):
            if Numer.num2text(i) == text:
                return i

    @staticmethod
    def date2text(date):
        day, month, year = date.split('.')
        text = ''
        if day[0] == '0':
            day_ = Numer.num2text(int(day[1])) + str(Numer.endings[int(day[1])])
        else:
            if day[1] == '0':
                day_ = Numer.num2text(int(day)) + str(Numer.endings2[int(day[0]) - 1])
            else:
                day_ = Numer.num2text(int(day)) + str(Numer.endings[int(day[1])])

        if month[0] == '0':
            month_ = month[1]
        else:
            month_ = month

        text += Numer.num2text(int(year), 'жылғы') + ' '
        text += day_ + ' '
        text += Numer.months[int(month_) - 1]
        return text

    ROMAN_NUMERAL_TABLE = [
        ("M", 1000), ("CM", 900), ("D", 500),
        ("CD", 400), ("C", 100), ("XC", 90),
        ("L", 50), ("XL", 40), ("X", 10),
        ("IX", 9), ("V", 5), ("IV", 4),
        ("I", 1)
    ]

    @staticmethod
    def num2roman(number):
        roman_numerals = []
        for numeral, value in Numer.ROMAN_NUMERAL_TABLE:
            count = number // value
            number -= count * value
            roman_numerals.append(numeral * count)

        return ''.join(roman_numerals)

    @staticmethod
    def roman2numITER(rom):
        if type(rom) == str:
            rom = rom.upper()
            for i in range(0, 100000):
                if Numer.num2roman(i) == rom:
                    return i
        return None

    @staticmethod
    def is_roman(rom):
        if Numer.roman2numITER(rom) is None:
            return False
        else:
            return True


if __name__ == '__main__':
    num = 2015
    print(Numer.date2text('23.07.2020'))
    print(Numer.num2text(num), Numer.text2numITER(Numer.num2text(num)))
    print(Numer.num2roman(num), Numer.roman2numITER(Numer.num2roman(num)))
    print(Numer.is_roman('XXXX'))
