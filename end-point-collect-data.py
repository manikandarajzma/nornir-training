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
    request_url = '/node/class/fvTenant.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
    tenant_data = json.loads(response_data.text)
    #print(tenant_data)
    tenant_list = []

    for  data in tenant_data['imdata']:
        tenant_list.append(data['fvTenant']['attributes']['name'])
  
    #print(tenant_list)
    #request_url = '/node/mo/uni/tn-MBDC.json?query-target=children&target-subtree-class=fvAp'
    #response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
    #ap_data = json.loads(response_data.text)
    
    for tenant in tenant_list:    
        ap_list = []
        request_url = '/node/mo/uni/tn-' + tenant + '.json?query-target=children&target-subtree-class=fvAp'
        response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
        ap_data = json.loads(response_data.text)
        
        for data in ap_data['imdata']:
            #print(request_url)
            ap_list.append(data['fvAp']['attributes']['name'])
            epg_list = []
            for ap in ap_list:
                request_url = '/node/mo/uni/tn-' + tenant + '/ap-' + ap + '.json?query-target=subtree&target-subtree-class=fvAEPg'
                response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
                epg_data = json.loads(response_data.text)
                #print(epg_data)
                for data in epg_data['imdata']:
                    try:
                       # print(request_url)
                        epg_list.append(data['fvAEPg']['attributes']['name'])
                        #print(epg_list)
                    except:
                        print("something  wrong")
                        
                    for epg in epg_list:
                        request_url = '/node/mo/uni/tn-' + tenant + '/ap-' + ap + '/epg-' + epg + '.json?query-target=children&target-subtree-class=fvCEp&rsp-subtree=children&rsp-subtree-class=fvRsToVm,fvRsVm,fvRsHyper,fvRsCEpToPathEp,fvIp,fvPrimaryEncap'  
                        #request_url = '/node/mo/uni/tn-MBDC/ap-MBDC_AppProf/epg-AH_Philips_1299_EPG.json?query-target=children&target-subtree-class=fvCEp&rsp-subtree=children&rsp-subtree-class=fvRsToVm,fvRsVm,fvRsHyper,fvRsCEpToPathEp,fvIp,fvPrimaryEncap'
                        response_data = requests.get(base_url + request_url, cookies=cookies, verify = False )
                        ep_data = json.loads(response_data.text)
                        #print(ep_data)
                        for  data in ep_data['imdata']:
                            #print(data['fvCEp']['attributes']['encap'])       
                            #print(tenant,ap,epg)
                            ip_addr = data['fvCEp']['attributes']['ip']
                            #print(data['fvCEp']['attributes']['mac'])
                            #print(data['fvCEp']['children'])
                            print(ip_addr)
                            for i in data['fvCEp']['children']:
                                if 'fvRsCEpToPathEp' in i:
                                     #print(i)
                                     leaf = i['fvRsCEpToPathEp']['attributes']['rn'].split('/')[2].split('-')
                                     #print(leaf)
                                     if len(leaf) == 2:
                                        print("single homed")
                                        leaf = leaf[1]
                                     else:
                                        leaf = leaf[1] + '-'  + leaf[2]
                                     print(i)
                                     interface = i['fvRsCEpToPathEp']['attributes']['rn'].split('/')[3].split('pathep-')[1]

                                     #leaf = i.split('/')[2].split('-')[1] + '-' + i.split('/')[2].split('-')[2]
                                     #interface = i.split('/')[3].split('-')[1]
                                     print(leaf,interface)
                            #if ip_addr == '0.0.0.0':
                               # print(data['fvCEp']['children'][0]['fvRsCEpToPathEp']['attributes']['rn'])
                            #elif 'fvIp' in data['fvCEp']['children'][1]:
                                #print(data)
                                #print(data['fvCEp']['children'][2]['fvRsCEpToPathEp']['attributes']['rn'])
                            #else:
                                #print(data['fvCEp']['children'][1]['fvRsCEpToPathEp']['attributes']['rn'])

                            #if ip_addr == '0.0.0.0':
                              # print("Ip is all zero")
                               #print(data['fvCEp']['children'][1]['fvRsCEpToPathEp']['attributes']['rn'])
                               #print(data['fvCEp']['children'][0]['fvRsCEpToPathEp']['attributes']['rn'])                               
                            #else:
                               #print("IP is non zero")
                               #print(data)
                               #print(data['fvCEp']['children'][1]['fvRsCEpToPathEp']['attributes']['rn'])
                               #print(data[1]['fvRsCEpToPathEp']['attributes']['rn'].split('/')[2].split('-')[1] + '-' +  data[1]['fvRsCEpToPathEp']['attributes']['rn'].split('/')[2].split('-')[2])
                            #interface = data[1]['fvRsCEpToPathEp']['attributes']['rn'].split('/')[3].split('-')[1]
                            #print(leaf)
                            #leaf = data[1]['fvRsCEpToPathEp']['attributes']['rn'].split('/')[2].split('-')[1] + '-' +  data[1]['fvRsCEpToPathEp']['attributes']['rn'].split('/')[2].split('-')[2]
                            #leaf =  data['fvCEp']['children'][1]['fvRsCEpToPathEp']['attributes']['rn']
                            #print(leaf) 

                            

                            
#create_end_point_table(base_url, cookies)
create_ep_table(base_url,cookies)

 
