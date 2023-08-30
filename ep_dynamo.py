import json
import psycopg2
from datetime import datetime
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


# reading the data from the file


conn = psycopg2.connect(database = "aci", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5433)
cur = conn.cursor()
# drop_table_endpoint_data = ''' DROP table IF EXISTS endpoint_data '''
# cur.execute(drop_table_endpoint_data)
# cur.execute("""CREATE TABLE endpoint_data(
#             epg_name VARCHAR(1000),
#             vlan VARCHAR(50)  NOT NULL,
#             ip_address VARCHAR(100) NOT NULL,
#             mac_address VARCHAR(100) NOT NULL);
#             """)

# drop_table_endpoint_count = ''' DROP table IF EXISTS endpoint_count '''
# cur.execute(drop_table_endpoint_count)
# cur.execute("""CREATE TABLE endpoint_count(
#              ep_count VARCHAR(50));
#             """)

# ep_number = ep_data['totalCount']
# cur.execute("INSERT INTO endpoint_count (ep_count) values (%s)", (ep_number, ));

# cur.execute("INSERT INTO endpoint_graph values (%s, %s)", (ep_number, date_time));
# for data in ep_data['imdata']:
#   for ep in data['fvCEp'].items():
#        ep_dn = ep[1]['dn']   
#        epg = ep_dn.split('/')[3].split('-')[1]
#        vlans = ep[1]['encap']
#        ip = ep[1]['ip']
#        mac = ep[1]['mac']
#        cur.execute("INSERT INTO endpoint_data values (%s,%s,%s,%s)", (epg, vlans, ip, mac));

def count_ep(cur):
    with open('ep_data.json') as f:
        ep_data = json.load(f)
    ep_count = ep_data['totalCount']
    drop_table_ep_count = ''' DROP table IF EXISTS ep_count '''
    cur.execute(drop_table_ep_count)
    cur.execute("""CREATE TABLE ep_count(
             ep_count VARCHAR(50));
            """)
    cur.execute("INSERT INTO ep_count (ep_count) values (%s)", (ep_count, ));
    
    ''' EP graph'''

    cur.execute("""CREATE TABLE IF NOT EXISTS ep_count_graph(
            ep_count SERIAL,
            dateadded varchar(100000));
        """)
    cur.execute("INSERT INTO ep_count_graph values (%s, %s)", (ep_count, date_time));

    ''' EP table '''
    drop_table_endpoint_data = ''' DROP table IF EXISTS endpoint_data '''
    cur.execute(drop_table_endpoint_data)
    cur.execute("""CREATE TABLE endpoint_data(
                epg_name VARCHAR(1000),
                vlan VARCHAR(50)  NOT NULL,
                ip_address VARCHAR(100) NOT NULL,
                mac_address VARCHAR(100) NOT NULL);
                """)
    
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

    ''' BD table '''
    drop_table_BD_data = ''' DROP table IF EXISTS BD_data '''
    cur.execute(drop_table_BD_data)
    cur.execute("""CREATE TABLE BD_data(
                tenant VARCHAR(1000),
                BD_name VARCHAR(50)  NOT NULL,
                intersiteBumTrafficAllow VARCHAR(100) NOT NULL,
                intersiteL2Stretch VARCHAR(100) NOT NULL,
                ipLearning VARCHAR(100) NOT NULL,
                pcTag VARCHAR(100) NOT NULL,
                unicastRoute VARCHAR(100) NOT NULL);
                """)
    
    for data in BD_data['imdata']:
      for BD in data['fvBD'].items():
        tenant = BD[1]['dn'].split('/')[1].split('-')[1]
        BD_name = BD[1]['dn'].split('/')[2].split('-')[1]
        intersiteBumTrafficAllow = BD[1]['intersiteBumTrafficAllow']
        intersiteL2Stretch = BD[1]['intersiteL2Stretch']
        ipLearning = BD[1]['ipLearning']
        pcTag = BD[1]['pcTag']
        unicastRoute = BD[1]['unicastRoute']
        cur.execute("INSERT INTO BD_data values (%s,%s,%s,%s,%s,%s,%s)", (tenant,BD_name,intersiteBumTrafficAllow,intersiteL2Stretch,ipLearning,pcTag,unicastRoute));

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

    ''' AP Count graph'''
    cur.execute("""CREATE TABLE IF NOT EXISTS AP_count_graph(
            AP_count SERIAL,
            dateadded varchar(100000));
        """)
    cur.execute("INSERT INTO AP_count_graph values (%s, %s)", (AP_count, date_time));


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

    ''' EPG Count graph'''
    cur.execute("""CREATE TABLE IF NOT EXISTS epg_count_graph(
            epg_count SERIAL,
            dateadded varchar(100000));
        """)
    cur.execute("INSERT INTO epg_count_graph values (%s, %s)", (epg_count, date_time));

    ''' EPG Table'''
    drop_table_epg_data = ''' DROP table IF EXISTS epg_data '''
    cur.execute(drop_table_epg_data)
    cur.execute("""CREATE TABLE epg_data(
                epg_name VARCHAR(1000),
                vlan VARCHAR(50)  NOT NULL,
                ip_address VARCHAR(100) NOT NULL,
                mac_address VARCHAR(100) NOT NULL);
                """)
    for data in epg_data['imdata']:
        for epg in data['fvAEPg'].items():
            tenant = epg[1]['dn'].split('/')[1].split('-')[1]
            AP = epg[1]['dn'].split('/')[2].split('-')[1]
            EPG_Name = epg[1]['dn'].split('/')[3].split('-')[1]
            pc_tag = epg[1]['pcTag']
            cur.execute("INSERT INTO epg_data values (%s,%s,%s,%s)", (tenant, AP, EPG_Name, pc_tag));


# count_ep(cur)
#count_tenant(cur)
count_BD(cur)
# count_AP(cur)
#count_epg(cur)
conn.commit()
cur.close()
conn.close()

