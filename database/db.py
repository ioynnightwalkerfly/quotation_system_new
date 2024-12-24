import sqlite3

# เชื่อมต่อฐานข้อมูล
def connect_db():
    return sqlite3.connect('quotation_system.db')

# สร้างตารางฐานข้อมูล
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # ตารางลูกค้า
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT
    )
    ''')

    # ตารางสินค้า
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        unit TEXT NOT NULL
    )
    ''')

    # ตารางใบเสนอราคา
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
    ''')

    # ตารางรายละเอียดใบเสนอราคา
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotation_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quotation_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (quotation_id) REFERENCES quotations (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    conn.commit()
    conn.close()

# ฟังก์ชันการจัดการลูกค้า
def add_customer(name, email, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, email, address) VALUES (?, ?, ?)", (name, email, address))
    conn.commit()
    conn.close()

def get_customers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_customer(customer_id, name, email, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, email = ?, address = ? WHERE id = ?", (name, email, address, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()

# ฟังก์ชันการจัดการสินค้า
def add_product(name, price, unit):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, unit) VALUES (?, ?, ?)", (name, price, unit))
    conn.commit()
    conn.close()

def get_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_product(product_id, name, price, unit):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, price = ?, unit = ? WHERE id = ?", (name, price, unit, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# ฟังก์ชันการจัดการใบเสนอราคา
def add_quotation(customer_id, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quotations (customer_id, date) VALUES (?, ?)", (customer_id, date))
    quotation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return quotation_id

def add_quotation_detail(quotation_id, product_id, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quotation_details (quotation_id, product_id, quantity) VALUES (?, ?, ?)", 
                   (quotation_id, product_id, quantity))
    conn.commit()
    conn.close()

def get_quotations():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT q.id, c.name, q.date 
    FROM quotations q
    JOIN customers c ON q.customer_id = c.id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_quotation_details(quotation_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT p.name, qd.quantity, p.price 
    FROM quotation_details qd
    JOIN products p ON qd.product_id = p.id
    WHERE qd.quotation_id = ?
    ''', (quotation_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_quotation(quotation_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quotation_details WHERE quotation_id = ?", (quotation_id,))
    cursor.execute("DELETE FROM quotations WHERE id = ?", (quotation_id,))
    conn.commit()
    conn.close()




def delete_quotation(quotation_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quotation_details WHERE quotation_id = ?", (quotation_id,))
    cursor.execute("DELETE FROM quotations WHERE id = ?", (quotation_id,))
    conn.commit()
    conn.close()
