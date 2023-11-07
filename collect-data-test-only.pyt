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




def create_ep_table(base_url,cookies):
    request_url = '/node/mo/uni/tn-MBDC/ap-MBDC_AppProf/epg-AH_Philips_1299_EPG.json?query-target=children&target-subtree-class=fvCEp&rsp-subtree=children&rsp-subtree-class=fvRsToVm,fvRsVm,fvRsHyper,fvRsCEpToPathEp,fvIp,fvPrimaryEncap'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
    ep_data = json.loads(response_data.text)
    #print(epg_data)

    for  data in ep_data['imdata']:
       for ep in data.items():
           print(ep['fvCEp])
           print('-'*50)
       #for ep in data['fvCEp'].items():
           #print(type(ep[1]))
           #print('-'*50)

#create_end_point_table(base_url, cookies)
create_ep_table(base_url,cookies)

