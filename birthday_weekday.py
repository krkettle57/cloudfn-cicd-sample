from enum import IntEnum, auto


class Weekday(IntEnum):
    SAT = 0
    SUN = auto()
    MON = auto()
    TUE = auto()
    WED = auto()
    THU = auto()
    FRI = auto()


def get_birthday_weekday(year: int, month: int, day: int) -> Weekday:
    # ref: https://en.wikipedia.org/wiki/Zeller%27s_congruence
    if month in (1, 2):
        year -= 1
        month += 12
    C = int(year / 100)
    Y = year % 100
    h = day + int(26 * (month + 1) / 10) + Y + int(Y / 4) - 2 * C + int(C / 4)
    X = h % 7
    return Weekday(X)
