import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(database = "aci", 
                            user = "postgres", 
                            host= 'localhost',
                            password = "postgres",
                            port = 5433)
    return conn

@app.route('/tables')
def tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM endpoint_data;')
    eps = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('eps.html',title = 'Endpoints Table', eps=eps)


