import psycopg2
from config import postgres_username, postgres_password

connection = None
cursor = None


def init_db():
    global connection
    connection = psycopg2.connect(database="postgres", user=postgres_username,
                                  password=postgres_password, host="127.0.0.1", port="5432")

    global cursor
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS CATEGORIES
        (ID         SERIAL  PRIMARY KEY,
        NAME        TEXT    NOT NULL);
        ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS PRODUCTS
        (ID         SERIAL  PRIMARY KEY,
        NAME        TEXT    NOT NULL,
        PRICE       INT     NOT NULL,
        CATEGORY    INTEGER REFERENCES CATEGORIES);
        ''')

    connection.commit()

    cursor.execute("INSERT INTO CATEGORIES (NAME) VALUES('food')")
    cursor.execute("INSERT INTO CATEGORIES (NAME) VALUES('electronics')")
    cursor.execute("INSERT INTO CATEGORIES (NAME) VALUES('dress')")

    connection.commit()


def update_product(id, product):
    global cursor
    cursor.execute(
        f"UPDATE PRODUCTS SET NAME='{product['name']}', PRICE={product['price']}, CATEGORY={product[category]} WHERE id={id} RETURNING *")

    global connection
    connection.commit()

    updated_product = cursor.fetchone()

    return rows_to_json(updated_product)


def insert_product(product):
    global cursor
    cursor.execute(
        f"SELECT ID FROM CATEGORIES WHERE NAME = '{product['category']}' ")

    category_id = cursor.fetchone()

    if category_id is None:
        raise Exception(f"Could not find the category: {product['category']}")

    category_id = category_id[0]

    sql = f"INSERT INTO PRODUCTS (NAME, PRICE, CATEGORY) VALUES('{product['name']}', {product['price']}, {category_id}) RETURNING *"

    cursor.execute(sql)

    global connection
    connection.commit()

    inserted_product = cursor.fetchone()

    return rows_to_json(inserted_product)


def find_product_by_id(id):
    global cursor
    cursor.execute(f"SELECT * from PRODUCTS p WHERE p.id={id}")

    row = cursor.fetchone()

    return rows_to_json(row)


def find_products(category=None):
    global cursor
    sql = "SELECT p.id, p.name, p.price, c.name from PRODUCTS p JOIN CATEGORIES c ON p.category=c.id"

    if category is not None:
        sql = f"{sql} AND c.name='{category}'"

    cursor.execute(sql)

    rows = cursor.fetchall()

    return rows_to_json(rows)


def delete_product(id):
    global cursor
    cursor.execute(f"DELETE FROM PRODUCTS WHERE id = {id}")
    cursor.commit()

    return

# helper


def rows_to_json(rows):
    lines = []

    if not isinstance(rows, list):
        rows = [rows]

    for row in rows:
        line = {"id": row[0], "name": row[1],
                "price": row[2], "category": row[3]}
        lines.append(line)

    return lines
