from flask import Flask, render_template,request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app= Flask(__name__)

app.secret_key = 'bunmi123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bunmi123'
app.config['MYSQL_DB'] = 'user'

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/inventory_form")
def inventory_form():
    return render_template('inventory_form.html')
