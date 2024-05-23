from typing import Iterable
from django.db.backends.utils import CursorWrapper
from collections import namedtuple


def get_and_string_from_iterable(iterable: Iterable) -> str:
    return ', '.join(iterable[:-1]) + f' and {iterable[-1]}' if len(iterable) >= 2 else iterable[-1]


def get_or_string_from_iterable(iterable: Iterable) -> str:
    return ', '.join(iterable[:-1]) + f' or {iterable[-1]}' if len(iterable) >= 2 else iterable[-1]


def dictfetchall(cursor: CursorWrapper) -> list:
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor: CursorWrapper) -> dict:
    "Return first row from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchone()
    if not rows:
        return {}
    return dict(zip(columns, rows))


def custom_named_tuple(**kwargs):
    CustomNamedTuple = namedtuple('CustomNamedTuple', kwargs.keys())
    return CustomNamedTuple(*kwargs.values())