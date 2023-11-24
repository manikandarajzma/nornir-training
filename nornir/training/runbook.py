from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def random_config(task):
    print(task.host['ntp_server'])
    command_list = [f"ntp server {task.host['ntp_server']}", "interface loopback0", f"ip address {task.host['loopback']} 255.255.255.255"]
    task.run(task=netmiko_send_config, config_file= 'netmiko_config_file.txt')

results = nr.run(task=random_config)
print_result(results)