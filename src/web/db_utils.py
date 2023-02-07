from django.db.models import Func, F
from django.db.models.expressions import RawSQL


class SplitPartFunc(Func):

    # F - позволяет обратиться к полю объекта, Func - вызов чистой ф-ии на sql
    def __init__(self, field_name: str, delimiter: str, number: int, *expressions, **extra):
        super().__init__(F(field_name), RawSQL("%s", [delimiter]), RawSQL("%s", [number]), function="split_part")
