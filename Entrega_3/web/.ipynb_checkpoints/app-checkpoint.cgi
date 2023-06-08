#!/usr/bin/python3

from wsgiref.handlers import CGIHandler

from flask import Flask
from flask import render_template, request, redirect, url_for
from urllib.parse import quote, unquote

"""
## Libs postgres
import psycopg2
import psycopg2.extras
"""

app = Flask(__name__)

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist1100032" 
DB_DATABASE = DB_USER
DB_PASSWORD = ""
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)


@app.route("/")
def homepage():
    return render_template("base.html")


CGIHandler().run(app)