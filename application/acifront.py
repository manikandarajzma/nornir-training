import os
import psycopg2
from flask import Flask, render_template
import json
from datetime import datetime


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(database = "aci", 
                            user = "aciuser", 
                            host= 'localhost',
                            password = "acip@sswd",
                            port = 5432)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ep_count;')
    epcount = cur.fetchone()
    cur.execute('SELECT ep_count FROM ep_count_graph;')
    endpointcount = cur.fetchall()
    endpointcount = [x[0] for x in endpointcount]
    cur.execute('SELECT dateadded FROM ep_count_graph;')
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

    ''' Tenant graph '''
    cur.execute('SELECT tenant_count FROM tenant_count_graph;')
    tenantgraphcount = cur.fetchall()
    tenantgraphcount = [x[0] for x in tenantgraphcount]
    cur.execute('SELECT dateadded FROM tenant_count_graph;')
    tenantgraphcount_timestamp = cur.fetchall()
    tenantgraphcount_timestamp = [x[0] for x in tenantgraphcount_timestamp]
    tenantgraphcount_cleaned_timestamp = []
    for tenantgraphcount_cleanedentry in tenantgraphcount_timestamp:
         tenantgraphcount_cleaned_timestamp.append(datetime.strptime(tenantgraphcount_cleanedentry, '%m/%d/%Y, %H:%M:%S'))
    
    ''' BD graph '''
    cur.execute('SELECT BD_count FROM BD_count_graph;')
    BDgraphcount = cur.fetchall()
    BDgraphcount = [x[0] for x in BDgraphcount]
    cur.execute('SELECT dateadded FROM BD_count_graph;')
    BDgraphcount_timestamp = cur.fetchall()
    BDgraphcount_timestamp = [x[0] for x in BDgraphcount_timestamp]
    BDgraphcount_cleaned_timestamp = []
    for BDgraphcount_cleanedentry in BDgraphcount_timestamp:
         BDgraphcount_cleaned_timestamp.append(datetime.strptime(BDgraphcount_cleanedentry, '%m/%d/%Y, %H:%M:%S'))

    ''' AP graph '''
    cur.execute('SELECT AP_count FROM AP_count_graph;')
    APgraphcount = cur.fetchall()
    APgraphcount = [x[0] for x in APgraphcount]
    cur.execute('SELECT dateadded FROM AP_count_graph;')
    APgraphcount_timestamp = cur.fetchall()
    APgraphcount_timestamp = [x[0] for x in APgraphcount_timestamp]
    APgraphcount_cleaned_timestamp = []
    for APgraphcount_cleanedentry in APgraphcount_timestamp:
         APgraphcount_cleaned_timestamp.append(datetime.strptime(APgraphcount_cleanedentry, '%m/%d/%Y, %H:%M:%S'))

    ''' EPG graph '''
    cur.execute('SELECT epg_count FROM epg_count_graph;')
    epggraphcount = cur.fetchall()
    epggraphcount = [x[0] for x in epggraphcount]
    cur.execute('SELECT dateadded FROM epg_count_graph;')
    epggraphcount_timestamp = cur.fetchall()
    epggraphcount_timestamp = [x[0] for x in epggraphcount_timestamp]
    epggraphcount_cleaned_timestamp = []
    for epggraphcount_cleanedentry in epggraphcount_timestamp:
         epggraphcount_cleaned_timestamp.append(datetime.strptime(epggraphcount_cleanedentry, '%m/%d/%Y, %H:%M:%S'))

    cur.close()
    conn.close()
    return render_template('index.html', epcount=epcount, tenantgraphcount=tenantgraphcount,BDgraphcount=BDgraphcount,APgraphcount=APgraphcount,epggraphcount=epggraphcount,epg_count=epg_count,endpointcount=endpointcount,
                           tenant_count=tenant_count,BD_count=BD_count,AP_count=AP_count,cleaned_timestamp=cleaned_timestamp,tenantgraphcount_cleaned_timestamp=tenantgraphcount_cleaned_timestamp,BDgraphcount_cleaned_timestamp=BDgraphcount_cleaned_timestamp,
                           APgraphcount_cleaned_timestamp=APgraphcount_cleaned_timestamp,epggraphcount_cleaned_timestamp=epggraphcount_cleaned_timestamp)

    
@app.route('/eptables')
def eptables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM endpoints_data;')
    eps = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('ep-data.html',title = 'Endpoints Table', eps=eps)

@app.route('/epgtables')
def epgtables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM epg_data;')
    epgs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('epg-data.html',title = 'EPG Table', epgs=epgs)

@app.route('/BDtables')
def BDtables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM BD_data;')
    BDs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('BD-data.html',title = 'BD Table', BDs=BDs)


if __name__ == "__main__":
    #app.run(debug = True)
    app.run(host = '0.0.0.0')
