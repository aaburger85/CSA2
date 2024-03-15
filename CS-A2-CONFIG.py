from netmiko import ConnectHandler
import datetime as dt
import sys
import time
import os
print ('argument list', sys.argv)
switch_ip = sys.argv[1]
switch_username = sys.argv[2]
switch_password = sys.argv[3]
####
net_connect = ConnectHandler(
    device_type="cisco_xe",
    host= switch_ip,
    username=switch_username,
    password=switch_password,
)
####
check_service_internal = net_connect.send_command("show run | inc service internal")
if "service internal" in check_service_internal:
    print ("Service Intenal Enabled")
else:
    print ("Service internal is disabled, enabling service internal")
    net_connect.send_config_set('service internal')
while True:
    print()
    selection = input("Which would you like to do?\n(a) Poke switch config?\n(b) Check Status?\n(c) Delete config and log?\n(d) capture details for bug triage?\n").lower()
    print (f"You chose: {selection}")
    if "a" in selection:
        gethash = net_connect.send_command("test platform software config updater get")
        hashvalue = net_connect.send_command("more flash:meraki/md5hash")
        print ("waiting 5 seconds then poking dashboard for config upload")
        time.sleep(5)
        getcfgurl = net_connect.send_command("test platform software config updater dashboard get-cfg-url" + " " + hashvalue)
        print ("waiting 20 seconds then setting switch config cloud ready")
        time.sleep(15)
        gethash = net_connect.send_command("test platform software config updater get")
        time.sleep(2)
        hashvalue = net_connect.send_command("more flash:meraki/md5hash")
        time.sleep(2)
        pokeconfig = net_connect.send_command("test platform software config updater device cloud-cfg-rdy" + " " + hashvalue)
        print(pokeconfig)
        isconfigonbox = net_connect.send_command("more flash:/meraki/config_updater/monitor/dwnld_running.config | count .*")
        print ("config size is...")
        print (isconfigonbox)
    elif "b" in selection:
        output = net_connect.send_command("show meraki connect")
        output2 = net_connect.send_command("show meraki conf up")
        output3 = net_connect.send_command("more flash:meraki/config_updater/updater_err.xml")
        print (output)
        print (output2)
        if "Apply running config: Fail" in output2:
            print ("Config deploy failed")
            for line in output3.split('\n'):
                if "bad-command" in line:
                    print (line)
                else:
                    print (output3)
    elif "c" in selection:
        print ("Deleting downloaded config...")
        killconfig = net_connect.send_command("delete /force flash:/meraki/config_updater/monitor/dwnld_running.config")
        print ("Deleting config downloaded and error file...")
        killlog = net_connect.send_command("delete /force flash:meraki/config_updater/updater_err.xml")
    elif "d" in selection:
        dir_path = './debug_files'
        os.makedirs(dir_path, exist_ok=True)
        dtcurrent = dt.datetime.now()
        currenttime = dtcurrent.strftime("%m-%d-%Y-%H-%M-%S")
        filename = switch_ip+"-"+currenttime+".txt"
        file_path = os.path.join(dir_path, filename)
        print ("Grabbing config...")
        getconfig = net_connect.send_command("show run")
        time.sleep(1)
        print ("Grabbing version...")
        getversion = net_connect.send_command("show version")
        time.sleep(1)
        print ("Grabbing error xmls...")
        updateerr = net_connect.send_command("more flash:meraki/config_updater/updater_err.xml")
        time.sleep(1)
        print ("Grabbing downloaded xml config...")
        downloadedconfig = net_connect.send_command("more flash:meraki/config_updater/monitor/dwnld_running.config")
        time.sleep(1)
        f = open(file_path, 'x')
        print ("Grabbing running config xml...")
        getxmlconfig = net_connect.send_command("show run | format netconf-xml")
        time.sleep(1)
        runningversionbreak = "\n    \n##### SHOW VERSION #####\n     \n"
        time.sleep(1)
        runningconfigbreak = "\n    \n##### SHOW RUNNING CONFIGURATION #####\n    \n"
        time.sleep(1)
        runningxmlbreak = "\n     \n##### SHOW XML CONFIGURATION #####\n    \n"
        time.sleep(1)
        updateerrbreak = "\n     \n##### Update ERR XML #####\n    \n"
        time.sleep(1)
        downloadedconfigbreak = "\n     \n##### Downloaded XML #####\n    \n"
        print (f"Writing to file {filename}")
        f.write(runningversionbreak)
        f.write(getversion + "\n" *2)
        time.sleep(1)
        f.write(updateerrbreak)
        f.write(updateerr+ "\n" *2)
        time.sleep(1)
        f.write(downloadedconfigbreak)
        f.write(downloadedconfig + "\n" *2)
        time.sleep(1)
        f.write(runningconfigbreak)
        f.write(getconfig + "\n" *2)
        time.sleep(1)
        f.write(runningxmlbreak)
        time.sleep(1)
        f.write(getxmlconfig + "\n" *2)
        time.sleep(2)
        f.close()
                
    else:
        print ("Exiting due to no valid selection")
        break