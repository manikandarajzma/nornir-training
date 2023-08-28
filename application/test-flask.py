import os
import psycopg2
from flask import Flask, render_template
import json
from datetime import datetime


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(database = "aci", 
                            user = "postgres", 
                            host= 'localhost',
                            password = "postgres",
                            port = 5433)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM endpoint_count;')
    epcount = cur.fetchone()
    cur.execute('SELECT ep_count FROM endpoint_graph;')
    endpointcount = cur.fetchall()
    endpointcount = [x[0] for x in endpointcount]
    cur.execute('SELECT dateadded FROM endpoint_graph;')
    timestamp = cur.fetchall()
    timestamp = [x[0] for x in timestamp]
    cleaned_timestamp = []
    for cleanedentry in timestamp:
         cleaned_timestamp.append(datetime.strptime(cleanedentry, '%m/%d/%Y, %H:%M:%S'))
    cur.close()
    conn.close()
    return render_template('index.html', epcount=epcount, endpointcount=endpointcount,cleaned_timestamp=cleaned_timestamp)

@app.route('/eptables')
def eptables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM endpoint_data;')
    eps = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tables-data.html',title = 'Endpoints Table', eps=eps)


if __name__ == "__main__":
    app.run(debug = True)
