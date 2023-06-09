from flask import Flask
from flask import render_template, request
from flask import url_for, redirect

## Libs postgres
import psycopg2
import psycopg2.extras

app = Flask(__name__)

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist1100032" 
DB_DATABASE=DB_USER
DB_PASSWORD="projbd22-23"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

dbConn = psycopg2.connect(DB_CONNECTION_STRING)

@app.route('/')
def homepage():
    return render_template("base.html")


###########################################################
#########################CUSTOMERS#########################
###########################################################

@app.route('/customers')
def customers():
    """Show all the customers"""
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = "SELECT * FROM customer;"
        cursor.execute(query)
        return render_template("customers.html", customers=cursor)
    except Exception as e:
        return e #Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()
        
@app.route('/customers/new_customer')
def new_customer():
    try:
        return render_template("new_customer.html", params=request.args)
    except Exception as e:
        return str(e)

@app.route('/customers/new_customer/add', methods=["POST"])
def create_customer():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
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

        cursor.execute(query, data)
        
        return query
    except Exception as e:
        return str(e) 
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route('/customers/remove', methods=["POST"])
def remove_customer():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = """
            DELETE FROM customer
            WHERE cust_no = %(cust_no)s;
            """

        data = {
            "cust_no": request.form["cust_no"]
        }

        cursor.execute(query, data)
        
        return query
    except Exception as e:
        return str(e) 
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


###########################################################
#########################Products##########################
###########################################################


@app.route('/products')
def products():
    """Show all the products"""
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = "SELECT * FROM product;"
        cursor.execute(query)
        return render_template("products.html", products=cursor)
    except Exception as e:
        return e #Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route('/products/new_product')
def new_product():
    try:
        return render_template("new_product.html", params=request.args)
    except Exception as e:
        return str(e)

@app.route('/products/new_product/add', methods=["POST"])
def create_product():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
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

        cursor.execute(query, data)
        
        return query
    except Exception as e:
        return str(e) 
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route('/products/remove', methods=["POST"])
def remove_product():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = """
            DELETE FROM product
            WHERE SKU = %(SKU)s;
            """

        data = {
            "SKU": request.form["SKU"]
        }

        cursor.execute(query, data)
        
        return query
    except Exception as e:
        return str(e) 
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()
        
        
        
@app.route('/products/edit_product', methods=["POST"])
def edit_product():
    try:
        return render_template("edit_product.html", params=request.args)
    except Exception as e:
        return str(e)
    
@app.route('/products/edit_product/edit', methods=["POST"])
def edit_product_edit():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
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

        cursor.execute(query, data)
        
        return query
    except Exception as e:
        return str(e) 
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

if __name__ == '__main__':
    app.run(debug=True)