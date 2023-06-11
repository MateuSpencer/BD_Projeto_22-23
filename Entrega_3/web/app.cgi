#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist1100070"
DB_DATABASE = DB_USER
DB_PASSWORD = "tgpt8279"
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

@app.route('/suppliers/new_supplier')
def new_supplier():
    return render_template("new_supplier.html")

@app.route('/products/new_supplier/create', methods=["POST"])
def create_supplier():
    try:
        query = """
            INSERT INTO supplier (TIN, name, address, SKU, date)
            VALUES (%(TIN)s, %(name)s, %(address)s, %(SKU)s, %(date)s);
            """
        data = {
            "SKU": request.form["SKU"],
            "name": request.form["name"],
            "address": request.form["address"],
            "date": request.form["date"],
            "TIN": request.form["TIN"]
        }
        execute_query(query, data, fetch=False)
        return redirect(url_for('suppliers'))
    except Exception as e:
        return str(e)

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
            DELETE FROM pay WHERE order_no IN (SELECT order_no FROM orders WHERE cust_no = %(cust_no)s);
            DELETE FROM process WHERE order_no IN (SELECT order_no FROM orders WHERE cust_no = %(cust_no)s);
            DELETE FROM contains WHERE order_no IN (SELECT order_no FROM orders WHERE cust_no = %(cust_no)s);
            DELETE FROM orders WHERE cust_no = %(cust_no)s;
            DELETE FROM customer WHERE cust_no = %(cust_no)s;
            """
        data = {"cust_no": request.form["cust_no"]}
        execute_query(query, data, fetch=False)
        return redirect(url_for('customers'))
    except Exception as e:
        return str(e)
    
@app.route('/suppliers/remove', methods=["POST"])
def remove_supplier():
    try:
        query = """
            DELETE FROM supplier
            WHERE TIN = %(TIN)s;
            """
        data = {"TIN": request.form["TIN"]}
        execute_query(query, data, fetch=False)
        return redirect(url_for('suppliers'))
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
            DELETE FROM contains
            WHERE SKU = %(SKU)s;
            DELETE FROM supplier
            WHERE SKU = %(SKU)s;
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
    
@app.route('/suppliers')
def suppliers():
    try:
        query = "SELECT * FROM supplier;"
        suppliers = execute_query(query)
        return render_template("suppliers.html", suppliers=suppliers)
    except Exception as e:
        return str(e)
    
@app.route('/orders')
def orders():
    try:
        query = "SELECT * FROM orders;"
        orders = execute_query(query)
        query = "SELECT * FROM contains;"
        contains = execute_query(query)
        return render_template("orders.html", orders=orders, contains=contains)
    except Exception as e:
        return str(e)
    
@app.route('/products/new_order')
def new_order():
    return render_template("new_order.html")

@app.route('/orders/pay', methods=["POST"])
def pay_order():
    try:
        query = """
            INSERT INTO pay (order_no, cust_no)
            VALUES (%(order_no)s, %(cust_no)s);
            """
        data = {
            "order_no": request.form["order_no"],
            "cust_no": request.form["cust_no"],
        }
        execute_query(query, data, fetch=False)
        return redirect(url_for('orders'))
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    CGIHandler().run(app)