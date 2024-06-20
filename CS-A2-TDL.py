from netmiko import ConnectHandler
from argparse import ArgumentParser
import sys
print ('argument list', sys.argv)
switch_ip = sys.argv[1]
switch_username = sys.argv[2]
switch_password = sys.argv[3]
####
tdl_uri = ""
column_uri = ""
table_uri = ""
refactored_uri = tdl_uri.replace('?', '/')
refactored_column = column_uri.replace('?', '/')
refactored_table = table_uri.replace('?', '/')
###
#switch_ip = input ("Switch IP Address:")
#switch_username = input ("admin username:")
#switch_password = input ("admin password:")
net_connect = ConnectHandler(
    device_type="cisco_xe",
    host= switch_ip,
    username=switch_username,
    password=switch_password,
)
check_service_internal = net_connect.send_command("show run | inc service internal")
if "service internal" in check_service_internal:
    print ("Service Intenal Enabled")
else:
    print ("Service internal is disabled, enabling service internal")
    net_connect.send_config_set('service internal')
while True: 
    print()
    selection = input("Which would you like to do?\n(a) Get Models?\n(b) Get Hierarchy?\n(c) Get Tables?\n(d) Get Records?\n(e) Get N Recursive(note: quite picky)").lower()
    print (f"You chose: {selection}")
    if "a" in selection:
        models = net_connect.send_command("show platform software ndbman swi act r0 models")
        filter = input("Enter filter(hit enter for all):")
        print()
        if filter == "":
            print(models)
        else: 
            for f in models.split('\n'):
                if filter in f:
                    print(f"  {f}")
    elif "b" in selection:
        tdl_uri = input ("tdl uri from models:")
        refactored_uri = tdl_uri.replace('?', '/')
        output = net_connect.send_command("show platform software ndbman swi act r0 database hi" + " " + refactored_uri)
        filter = input("Enter filter(hit enter for all):")
        print()
        if filter == "":
            print(output)
        else: 
            for f in output.split('\n'):
                if filter in f:
                    print(f"  {f}")
    elif "c" in selection:
        column_uri = input ("Column uri:")
        refactored_column = column_uri.replace('?', '/')
        output = net_connect.send_command("show platform software ndbman swi act r0 database ta" + " " + refactored_column)
        print (output)
    elif "d" in selection:
        record_uri = input ("Record uri:")
        refactored_record = record_uri.replace('?', '/')
        output = net_connect.send_command("show platform software ndbman swi act r0 database re" + " " + refactored_record)
        print (output)
    elif "e" in selection:
        record_uri = input ("Get N Recursive uri:")
        refactored_record = record_uri.replace('?', '/')
        output = net_connect.send_command("show platform software ndbman swi act r0 database get_n_recursive" + " " + refactored_record)
        print (output)
    else:
        print ("Exiting due to no valid selection")
        break
