import requests, json, re

apic_ip = 'sandboxapicdc.cisco.com'
apic_username = 'admin'
apic_password = '!v3G@!4@Y'
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

request_url = '/node/class/fvCEp.json'

response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )

structured_data = json.loads(response_data.text)

for data in structured_data['imdata']:
    for ep in data['lldpAdjEp'].items():
        print(lldpdata)
        print('-'* 50)