import json
import psycopg2
  
# reading the data from the file
with open('ep_data.json') as f:
    ep_data = json.load(f)

conn = psycopg2.connect(database = "aci", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5433)
cur = conn.cursor()
drop_table = ''' DROP table IF EXISTS endpoint_data '''
cur.execute(drop_table)
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
       #print(epg)
       cur.execute("INSERT INTO endpoint_data values (%s,%s,%s,%s)", (epg, vlans, ip, mac));
conn.commit()
cur.close()
conn.close()

