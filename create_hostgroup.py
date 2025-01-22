import re
import sys
from collections import defaultdict
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

host_dict = {}
host_dict["sites"] = {}
name = ""
typ = ""
dpe_domain = ""
file_etc_hosts = open("/etc/hosts", "r")
# file_etc_hosts = open("/root/netapps/aupotato/scripts/ospgl_hosts.txt", "r")
# file_etc_hosts = open("./sample_plk_hosts.txt", "r")
# file_etc_hosts = open("./wind_hosts.txt", "r")
content = file_etc_hosts.readlines()
for i in content:
    if "Cluster" in i:
        name = ""
        typ = ""
        dpe_domain = ""
    if "Dpe Domain:" in i and name != "":
        dpe_domain = re.findall(r"Dpe Domain: (\w+)", i)[0]
    if "Hostname:" in i:
        name = re.findall(r"Hostname: (\w+)", i)[0]
        typ = re.findall(r"Machine Type: (\w+)", i)[0]
    if "Mng" in i and name != "":
        host_ip = i.split(" ")[0]
        if dpe_domain not in host_dict["sites"].keys():
            host_dict["sites"][dpe_domain] = {}
        if typ not in host_dict["sites"][dpe_domain].keys():
            host_dict["sites"][dpe_domain][typ] = {}
        host_dict["sites"][dpe_domain][typ][name] = host_ip


# file_ansiblehosts = open("/etc/ansible/hosts", "a+")
# file_ansiblehosts = open("./apps/application_patch/scripts/sample_ansible_hosts.txt", "w")
file_ansiblehosts = open("./data/sample_ansible_hosts.txt", "a+")
# pp.pprint(len(host_dict["all_nodes"].keys()))

#RUN FOR LOOP ON DPE_DOMAIN
for site_name in host_dict["sites"].keys():
    for node_type in host_dict["sites"][site_name].keys():
        if node_type == "PSMF":
            file_ansiblehosts.writelines("[PSMF]\n")
            # print("[PSMF]\n")
            file_ansiblehosts.writelines(["    {0} ansible_host=\"{1}\"\n".format(ip, hostname) for ip, hostname in host_dict["sites"][site_name][node_type].items()])
        elif node_type == "MPPSMF":
            file_ansiblehosts.writelines("[MPPSMF]\n")
            # print("[MPPSMF]\n")
            file_ansiblehosts.writelines(["    {0} ansible_host=\"{1}\"\n".format(ip, hostname) for ip, hostname in host_dict["sites"][site_name]
            [node_type].items()])

file_ansiblehosts.writelines("[SLEE]\n")
# print("[SLEE]\n")
for site_name in host_dict["sites"].keys():
    file_ansiblehosts.writelines(["    {0} ansible_host=\"{1}\"\n".format(ip, hostname) for ip, hostname in host_dict["sites"][site_name]["SLEE"].items()])

print("host_dict")
print(host_dict)