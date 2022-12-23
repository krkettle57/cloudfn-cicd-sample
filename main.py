import functions_framework
from dateutil.parser import parse as date_parse
from flask import Request

from birthday_weekday import get_birthday_weekday


@functions_framework.http
def main(request: Request) -> str:
    request_args = request.args
    if not (request_args and "birthday" in request_args):
        return "'birthday' is required."

    try:
        birthday = date_parse(request.args["birthday"])
    except Exception:
        return "The format of 'birthday' is invalid."

    weekday = get_birthday_weekday(birthday.year, birthday.month, birthday.day)
    return f"{birthday.strftime('%Y-%m-%d')} is {weekday.name}"
