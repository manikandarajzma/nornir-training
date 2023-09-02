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
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5433)
cur = conn.cursor()


def create_end_point_table(base_url, cookies):
    request_url = '/node/class/fvCEp.json'

    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )

    ep_data = json.loads(response_data.text)
    ep_count = ep_data['totalCount']
    print(ep_count)
    # for data in ep_data['imdata']:
    #     for ep in data['fvCEp'].items():
    #         ep_dn = ep[1]['dn']   
    #         print(ep_dn.split('/')[3].split('-')[1])
    #         print(ep[1]['encap'])
    #         print(ep[1]['ip'])
    #         print(ep[1]['mac'])
    #         print('-'* 50)

create_end_point_table(base_url,cookies)

