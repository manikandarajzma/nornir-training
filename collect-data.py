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


def create_end_point_table(base_url, cookies):
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
 
    conn.commit()
    cur.close()
    conn.close()


create_end_point_table(base_url,cookies)

