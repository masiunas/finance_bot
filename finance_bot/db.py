"""DB."""
# === Standard library imports ===
import sqlite3
from typing import Dict, List, NoReturn

conn = sqlite3.connect('expenses.db')  # или :memory: чтобы сохранить в RAM
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_categories_table() -> NoReturn:
    """Create categories table."""
    cursor.execute("""CREATE TABLE categories
                      (
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
                       )
                   """)
    init_categories_table()


def create_expenses_table() -> NoReturn:
    """Create expense table."""
    cursor.execute("""CREATE TABLE expenses
                      (
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
                       )
                   """)


def create_budget_table() -> NoReturn:
    """Create budget table."""
    cursor.execute("""CREATE TABLE budget
                      (
    codename varchar(255) primary key,
    daily_limit integer
                       )
                   """)


def init_categories_table() -> NoReturn:
    """Init categories table."""
    cursor.execute("""
    INSERT INTO categories VALUES
    ("products", "продукты", "true", "еда"),
    ("coffee", "кофе", "true", ""),
    ("dinner", "обед", "true", "столовая, ланч, бизнес-ланч, бизнес ланч"),
    ("cafe", "кафе", "true", "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
    ("transport", "общ. транспорт", "false", "метро, автобус, metro"),
    ("taxi", "такси", "false", "яндекс такси, yandex taxi"),
    ("phone", "телефон", "false", "теле2, связь"),
    ("books", "книги", "false", "литература, литра, лит-ра"),
    ("internet", "интернет", "false", "инет, inet"),
    ("subscriptions", "подписки", "false", "подписка"),
    ("other", "прочее", "true", "");""")
    conn.commit()


def check_table_exist() -> NoReturn:
    """Check if table exist."""
    tables = {'categories': 'create_categories_table()',
              'budget': 'create_budget_table()',
              'expenses': 'create_expenses_table()'}
    for table in tables:
        # TODO: Fix possible sql injection from line below <Pavel 2020-01-15>
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(table))
        if cursor.fetchall():
            print('Table "{0}" already exist.'.format(table))
        else:
            # TODO: remove eval usage (consider using safer `ast.literal_eval`) <Pavel 2020-01-15>
            eval(tables.get(table))


def fetchall_values(table: str) -> List[Dict[str, str]]:
    """Fetchall Values."""
    # TODO: Fix possible sql injection from line below <Pavel 2020-01-15>
    cursor.execute('SELECT * FROM {0} '.format(table))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = dict(row)
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> NoReturn:
    """Delete."""
    row_id = int(row_id)
    # TODO: Fix possible sql injection from line below <Pavel 2020-01-15>
    cursor.execute(f'delete from {table} where id={row_id}')
    conn.commit()


check_table_exist()
