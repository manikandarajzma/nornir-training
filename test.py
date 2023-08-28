import requests, json, re

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

request_url = '/node/class/fvAp.json'

response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )

structured_data = json.loads(response_data.text)

print(structured_data)

#for data in structured_data['imdata']:
   #print(data)
  # for ep in data['fvCEp'].items():
      # ep_dn = ep[1]['dn']   
       #print(ep_dn.split('/')[3].split('-')[1])
       #print(ep[1]['encap'])
       #print(ep[1]['ip'])
       #print(ep[1]['mac'])
       #print('-'* 50)
