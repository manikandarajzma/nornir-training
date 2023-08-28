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
    ''' tenant count '''
    cur.execute('SELECT * FROM tenant_count;')
    tenant_count = cur.fetchone()

    ''' tenant count '''
    cur.execute('SELECT * FROM BD_count;')
    BD_count = cur.fetchone()

    ''' AP count '''
    cur.execute('SELECT * FROM AP_count;')
    AP_count = cur.fetchone()

    ''' EPG count '''
    cur.execute('SELECT * FROM epg_count;')
    epg_count = cur.fetchone()

    cur.close()
    conn.close()
    return render_template('index.html', epcount=epcount, epg_count=epg_count,endpointcount=endpointcount,tenant_count=tenant_count,BD_count=BD_count,AP_count=AP_count,cleaned_timestamp=cleaned_timestamp)

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
