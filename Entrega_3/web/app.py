from flask import Flask
from flask import render_template
from flask import url_for

## Libs postgres
import psycopg2
import psycopg2.extras

app = Flask(__name__)

## SGBD configswwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist1100032" 
DB_DATABASE=DB_USER
DB_PASSWORD="projbd22-23"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

dbConn = psycopg2.connect(DB_CONNECTION_STRING)

@app.route('/')
def homepage():
    return render_template("base.html")

@app.route('/customers')
def customers():
    """Show all the customers"""
    cursor = dbConn.cursor()
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    
    return render_template("customers.html", customers=customers)


if __name__ == '__main__':
    app.run(debug=True)