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

conn.commit()
cur.close()
conn.close()

