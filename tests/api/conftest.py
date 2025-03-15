import pytest
import psycopg2
from tests.api.settings import db_params


@pytest.fixture
def connect_to_db():
    """
    Фикстура коннекта к базе данных
    """
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.close()
