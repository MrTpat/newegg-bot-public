import time
import os
import requests
import colors
import glob
import configparser

def killVPN() -> None:
    os.system('killall openvpn &> /dev/null')

def getCurrIp() -> str:
    r = requests.get('https://api.ipify.org?format=json')
    if r.status_code != 200:
        colors.printFail('Failed to detect IP address, retrying...')
        time.sleep(1)
        return getCurrIp()
    else:
        colors.printInfo('detected IP: ' + r.json()['ip'])
        return r.text

def switchVPN(vpn_id: str, username: str, password: str) -> None:
    formerIP = getCurrIp()
    colors.printInfo('Swapping IP address...')
    killVPN()
    newConfigFile = getConfigFileName(vpn_id)
    res = os.system('./vpnConnector.sh ' + newConfigFile + ' ' + username + ' ' + password)
    if res != 0:
        colors.printFail('Failed to connect to VPN. Trying again...')
        switchVPN(vpn_id, username, password)
    else:
        time.sleep(10)
    if formerIP == getCurrIp():
        colors.printFail('Unsuccessful swap...trying again in 5 seconds')
        time.sleep(5)
        switchVPN(vpn_id, username, password)
    else:
        colors.printSuccess('Successful swap of IP address...')

def getConfigFileName(x: int) -> str:
    return glob.glob("/etc/openvpn/configurations/*")[x]

vpn_id = 0
vpn_max = 150
config = configparser.ConfigParser()
config.read('vpnConfig.ini')
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']
while True:
    if vpn_id > vpn_max:
        vpn_id = 0
    switchVPN(vpn_id, username, password)
    vpn_id = vpn_id + 1
    time.sleep(600)
