import requests, json, re
import psycopg2
from datetime import datetime
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")



apic_ip = 'mbdcapic1.multicare.org'
apic_username = 'admin'
apic_password = 'C1sco123'
credentials = {'aaaUser':
                {'attributes':
                    {'name': apic_username, 'pwd': apic_password }
                }
    }

base_url = 'https://%s/api/' % apic_ip





login_url = base_url + '/aaaLogin.json'

json_credentials = json.dumps(credentials)

post_response = requests.post(login_url, data=json_credentials, verify=False)

post_response_json = json.loads(post_response.text)
login_attributes = post_response_json['imdata'][0]['aaaLogin']['attributes']

cookies = {}
cookies['APIC-Cookie'] = login_attributes['token']

''' psql connection '''
conn = psycopg2.connect(database = "aci", 
                        user = "aciuser", 
                        host= 'localhost',
                        password = "acip@sswd",
                        port = 5432)
cur = conn.cursor()


def create_end_point_table(base_url, cookies,cur):
    request_url = '/node/class/fvCEp.json'

    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )

    ep_data = json.loads(response_data.text)
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

    
def create_tenant_table(base_url, cookies,cur):
    request_url = '/node/class/fvTenant.json'

    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )

    tenant_data = json.loads(response_data.text)
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


def create_BD_table(base_url, cookies,cur):
    request_url = '/node/class/fvBD.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
    BD_data = json.loads(response_data.text)

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

def create_AP_table(base_url, cookies,cur):
    request_url = '/node/class/fvAP.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
    AP_data = json.loads(response_data.text)

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


def create_epg_table(base_url,cookies,cur):
    request_url = '/node/class/fvAEPg.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
    epg_data = json.loads(response_data.text)

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



create_end_point_table(base_url,cookies,cur)
create_tenant_table(base_url,cookies,cur)
create_BD_table(base_url,cookies,cur)
create_AP_table(base_url,cookies,cur)
create_epg_table(base_url,cookies,cur)


conn.commit()
cur.close()
conn.close()
