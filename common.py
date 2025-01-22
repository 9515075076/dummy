import subprocess
import shlex
import paramiko as ssher
import os
from config import app_conf_json_path
from json import loads, dumps

def console_output(command):
    return str(subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE).communicate()[0].decode("utf-8")).split("\n")

def console_output_shell(command):
    return str(subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")).split("\n")

def test_platform_credenials(platform_ip, root_password, linus_password, toc_password="None"):
    with open(app_conf_json_path) as json_file:
        app_config = loads(json_file.read())
    
    platform_output = console_output("{0} {1} {2} {3} {4}".format(app_config["scripts"]["verify_passwords"], platform_ip, linus_password, toc_password, root_password))[:-1]
    if len(platform_output) == 1:
        return False, "The platform could not be reached!"
    else:
        print(platform_output)
        for line in platform_output:
            if "Permission denied, please try again." in line or "Error: Wrong login or password" in line or "su: incorrect password" in line:
                return False, "Error : One or more passwords are incorrect!"
            elif "Error:" in line:
                return False, "Error : {0}".format(line.split("Error:")[1].strip())
        return True, "All credentials verified!"

def verify_input(platform_ip, root_password, linus_password, toc_password="None"):
    with open(app_conf_json_path) as json_file:
        app_config = loads(json_file.read())

    platform_test_result, platform_test_message = test_platform_credenials ( 
        platform_ip 	= platform_ip,
        linus_password	=	linus_password,
        root_password 	=  	root_password,
        toc_password    =   toc_password
    )

    if not platform_test_result:
        return False, platform_test_message
    return True, platform_test_message

def get_installed_services(linus_password, active_smf):
    service_dict = {}
    
    command_output = console_output("./scripts/expect_services.sh {active_smf_name} {linus_password}".format(active_smf_name = active_smf, linus_password = linus_password))[:-1]
    

    for service in command_output:
        print("Printing Available Services*************",service)
        if service.split(",")[0] not in service_dict.keys():
            service_dict[service.split(",")[0]] = {}                
            service_dict[service.split(",")[0]]["hosts"] = []
        service_dict[service.split(",")[0]]["ri"] = service.split(",")[1]
        service_dict[service.split(",")[0]]["hosts"].append(service.split(",")[2])
    # print(service_dict)
    return service_dict