import sqlite3

conn = sqlite3.connect("expenses.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


def create_categories_table():
    cursor.execute("""CREATE TABLE categories
                      (
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
                       )
                   """)
    init_categories_table()


def create_expenses_table():
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


def create_budget_table():
    cursor.execute("""CREATE TABLE budget
                      (
    codename varchar(255) primary key,
    daily_limit integer
                       )
                   """)


def init_categories_table():
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
    ("other", "прочее", "true", "");
                      """
                   )
    conn.commit()


def check_table_exist():
    tables = {'categories': 'create_categories_table()', 'budget': 'create_budget_table()',
              'expenses': 'create_expenses_table()'}
    for table in tables:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table))
        if cursor.fetchall():
            print('Table "{}" already exist.'.format(table))
        else:
            eval(tables.get(table))


def fetchall_values(table: str) -> list:
    cursor.execute("SELECT * FROM {} ".format(table))
    values = cursor.fetchall()
    result = []
    for line in values:
        dict_row = {
            'codename': line[0],
            'name': line[1],
            'is_base_expense': line[2],
            'aliases': line[3],
        }
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


check_table_exist()
