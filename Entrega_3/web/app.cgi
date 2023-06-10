#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist1100032"
DB_DATABASE = DB_USER
DB_PASSWORD = "projbd22-23"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
    DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD
)

def execute_query(query, data=None, fetch=True):
    db_conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    if fetch:
        result = cursor.fetchall()
        cursor.close()
        db_conn.close()
        return result
    else:
        db_conn.commit()
        cursor.close()
        db_conn.close()

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/customers')
def customers():
    try:
        query = "SELECT * FROM customer;"
        customers = execute_query(query)
        return render_template("customers.html", customers=customers)
    except Exception as e:
        return str(e)

@app.route('/customers/new_customer')
def new_customer():
    return render_template("new_customer.html")

@app.route('/customers/new_customer/add', methods=["POST"])
def create_customer():
    try:
        query = """
            INSERT INTO customer (cust_no, name, email, phone, address)
            VALUES (%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s);
            """
        data = {
            "cust_no": request.form["cust_no"],
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "address": request.form["address"]
        }
        execute_query(query, data, fetch=False)
        return redirect(url_for('customers'))
    except Exception as e:
        return str(e)

@app.route('/customers/remove', methods=["POST"])
def remove_customer():
    try:
        query = """
            DELETE FROM customer
            WHERE cust_no = %(cust_no)s;
            """
        data = {"cust_no": request.form["cust_no"]}
        execute_query(query, data, fetch=False)
        return redirect(url_for('customers'))
    except Exception as e:
        return str(e)

@app.route('/products')
def products():
    try:
        query = "SELECT * FROM product;"
        products = execute_query(query)
        return render_template("products.html", products=products)
    except Exception as e:
        return str(e)

@app.route('/products/new_product')
def new_product():
    return render_template("new_product.html")

@app.route('/products/new_product/create', methods=["POST"])
def create_product():
    try:
        query = """
            INSERT INTO product (SKU, name, description, price, ean)
            VALUES (%(SKU)s, %(name)s, %(description)s, %(price)s, %(ean)s);
            """
        data = {
            "SKU": request.form["SKU"],
            "name": request.form["name"],
            "description": request.form["description"],
            "price": request.form["price"],
            "ean": request.form["ean"]
        }
        execute_query(query, data, fetch=False)
        return redirect(url_for('products'))
    except Exception as e:
        return str(e)

@app.route('/products/remove', methods=["POST"])
def remove_product():
    try:
        query = """
            DELETE FROM product
            WHERE SKU = %(SKU)s;
            """
        data = {"SKU": request.form["SKU"]}
        execute_query(query, data, fetch=False)
        return redirect(url_for('products'))
    except Exception as e:
        return str(e)

@app.route('/products/edit_product', methods=["POST"])
def edit_product():
    return render_template("edit_product.html")

@app.route('/products/edit_product/update', methods=["POST"])
def edit_product_update():
    try:
        query = """
            UPDATE product
            SET price = %(price)s, description = %(description)s
            WHERE SKU = %(SKU)s;
            """
        data = {
            "SKU": request.form["SKU"],
            "description": request.form["description"],
            "price": request.form["price"],
        }
        execute_query(query, data, fetch=False)
        return redirect(url_for('products'))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    CGIHandler().run(app)