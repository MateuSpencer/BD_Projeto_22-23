#!/usr/bin/python3
from logging.config import dictConfig

import psycopg2
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

# TODO: maybe especifico à outra app
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist1100032" 
DB_DATABASE=DB_USER
DB_PASSWORD=""
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

# try:
dbConn = psycopg2.connect(DB_CONNECTION_STRING)
cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)