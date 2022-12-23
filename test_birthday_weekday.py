from datetime import datetime

import pytest

from birthday_weekday import Weekday, get_birthday_weekday

birthday_weekday_pairs = [
    # abnormal case
    ("1999/12/31", Weekday.FRI),
    ("2000/01/01", Weekday.SAT),
    ("2000/02/29", Weekday.TUE),
    # year case
    ("2021/01/01", Weekday.FRI),
    ("2021/02/01", Weekday.MON),
    ("2021/03/01", Weekday.MON),
    ("2021/04/01", Weekday.THU),
    ("2021/05/01", Weekday.SAT),
    ("2021/06/01", Weekday.TUE),
    ("2021/07/01", Weekday.THU),
    ("2021/08/01", Weekday.SUN),
    ("2021/09/01", Weekday.WED),
    ("2021/10/01", Weekday.FRI),
    ("2021/11/01", Weekday.MON),
    ("2021/12/01", Weekday.WED),
    # week case
    ("2022/05/01", Weekday.SUN),
    ("2022/05/02", Weekday.MON),
    ("2022/05/03", Weekday.TUE),
    ("2022/05/04", Weekday.WED),
    ("2022/05/05", Weekday.THU),
    ("2022/05/06", Weekday.FRI),
    ("2022/05/07", Weekday.SAT),
]


@pytest.mark.parametrize("birthday, weekday", birthday_weekday_pairs)
def test_get_birthday_weekday(birthday: str, weekday: Weekday) -> None:
    birth_dt = datetime.strptime(birthday, "%Y/%m/%d")
    result = get_birthday_weekday(birth_dt.year, birth_dt.month, birth_dt.day)
    assert weekday == result
