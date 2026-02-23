from contextlib import contextmanager
from django.db import connection


@contextmanager
def cursor():
    with connection.cursor() as cur:
        yield cur


def execute(sql: str, params=None) -> None:
    with cursor() as cur:
        cur.execute(sql, params or [])


def fetchall(sql: str, params=None):
    with cursor() as cur:
        cur.execute(sql, params or [])
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
