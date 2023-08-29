import json
import psycopg2
from datetime import datetime
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


# reading the data from the file
with open('ep_data.json') as f:
    ep_data = json.load(f)

conn = psycopg2.connect(database = "aci", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5433)
cur = conn.cursor()
drop_table_endpoint_data = ''' DROP table IF EXISTS endpoint_data '''
cur.execute(drop_table_endpoint_data)
cur.execute("""CREATE TABLE endpoint_data(
            epg_name VARCHAR(1000),
            vlan VARCHAR(50)  NOT NULL,
            ip_address VARCHAR(100) NOT NULL,
            mac_address VARCHAR(100) NOT NULL);
            """)

drop_table_endpoint_count = ''' DROP table IF EXISTS endpoint_count '''
cur.execute(drop_table_endpoint_count)
cur.execute("""CREATE TABLE endpoint_count(
             ep_count VARCHAR(50));
            """)

ep_number = ep_data['totalCount']
cur.execute("INSERT INTO endpoint_count (ep_count) values (%s)", (ep_number, ));
cur.execute("INSERT INTO endpoint_graph values (%s, %s)", (ep_number, date_time));
for data in ep_data['imdata']:
  for ep in data['fvCEp'].items():
       ep_dn = ep[1]['dn']   
       epg = ep_dn.split('/')[3].split('-')[1]
       vlans = ep[1]['encap']
       ip = ep[1]['ip']
       mac = ep[1]['mac']
       cur.execute("INSERT INTO endpoint_data values (%s,%s,%s,%s)", (epg, vlans, ip, mac));

def count_tenant(cur):
    with open('tenant.json') as f:
       tenant_data = json.load(f)
    tenant_count = tenant_data['totalCount']
    drop_table_tenant_count = ''' DROP table IF EXISTS tenant_count '''
    cur.execute(drop_table_tenant_count)
    cur.execute("""CREATE TABLE tenant_count(
             tenant_count VARCHAR(50));
            """)
    cur.execute("INSERT INTO tenant_count (tenant_count) values (%s)", (tenant_count, ));
    
    ''' Tenant graph'''

    cur.execute("""CREATE TABLE IF NOT EXISTS tenant_count_graph(
            tenant_count SERIAL,
            dateadded varchar(100000));
        """)
    cur.execute("INSERT INTO tenant_count_graph values (%s, %s)", (tenant_count, date_time));

def count_BD(cur):
    with open('BD.json') as f:
       BD_data = json.load(f)
    BD_count = BD_data['totalCount']
    drop_table_BD_count = ''' DROP table IF EXISTS BD_count '''
    cur.execute(drop_table_BD_count)
    cur.execute("""CREATE TABLE BD_count(
             BD_count VARCHAR(50));
            """)
    cur.execute("INSERT INTO BD_count (BD_count) values (%s)", (BD_count, ));

    ''' BD Count graph'''
    cur.execute("""CREATE TABLE IF NOT EXISTS BD_count_graph(
            BD_count SERIAL,
            dateadded varchar(100000));
        """)
    cur.execute("INSERT INTO BD_count_graph values (%s, %s)", (BD_count, date_time));

def count_AP(cur):
    with open('AP.json') as f:
       AP_data = json.load(f)
    AP_count = AP_data['totalCount']
    drop_table_AP_count = ''' DROP table IF EXISTS AP_count '''
    cur.execute(drop_table_AP_count)
    cur.execute("""CREATE TABLE AP_count(
             AP_count VARCHAR(50));
            """)
    cur.execute("INSERT INTO AP_count (AP_count) values (%s)", (AP_count, ));

def count_epg(cur):
    with open('epg.json') as f:
       epg_data = json.load(f)
    epg_count = epg_data['totalCount']
    drop_table_epg_count = ''' DROP table IF EXISTS epg_count '''
    cur.execute(drop_table_epg_count)
    cur.execute("""CREATE TABLE epg_count(
             epg_count VARCHAR(50));
            """)
    cur.execute("INSERT INTO epg_count (epg_count) values (%s)", (epg_count, ));
    
count_tenant(cur)
count_BD(cur)
count_AP(cur)
count_epg(cur)
conn.commit()
cur.close()
conn.close()

