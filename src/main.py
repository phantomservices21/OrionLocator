current_version = 1.0

import os
from update_manager import canCheckForUpdates
from config_manager import checkForConfig
import requests_manager
import fade
from colorama import Fore
import re
from prettytable import PrettyTable
import json
from console_commands import *

regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

checkForConfig()

canCheckForUpdates()

os.system("cls")

print(
    fade.purplepink(
        rf"""
     /$$$$$$            /$$                     /$$                                       /$$                        
    /$$__  $$          |__/                    | $$                                      | $$                        
   | $$  \ $$  /$$$$$$  /$$  /$$$$$$  /$$$$$$$ | $$        /$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
   | $$  | $$ /$$__  $$| $$ /$$__  $$| $$__  $$| $$       /$$__  $$ /$$_____/ |____  $$|_  $$_/   /$$__  $$ /$$__  $$
   | $$  | $$| $$  \__/| $$| $$  \ $$| $$  \ $$| $$      | $$  \ $$| $$        /$$$$$$$  | $$    | $$  \ $$| $$  \__/
   | $$  | $$| $$      | $$| $$  | $$| $$  | $$| $$      | $$  | $$| $$       /$$__  $$  | $$ /$$| $$  | $$| $$      
   |  $$$$$$/| $$      | $$|  $$$$$$/| $$  | $$| $$$$$$$$|  $$$$$$/|  $$$$$$$|  $$$$$$$  |  $$$$/|  $$$$$$/| $$      
    \______/ |__/      |__/ \______/ |__/  |__/|________/ \______/  \_______/ \_______/   \___/   \______/ |__/ {Fore.GREEN}v{current_version}{Fore.WHITE}"""
    )
)


while True:
    ip_addr = input(f"{Fore.CYAN}[*] {Fore.GREEN}Enter the IP Address (Leave blank for your own):{Fore.WHITE} ").strip()
    
    if ip_addr == "":
        ip_addr = ""
        skip_regex = True
    else:
        skip_regex = False 

    if skip_regex or re.search(regex, ip_addr): 
        ip_request = requests_manager.get(f"http://ip-api.com/json/{ip_addr}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
        
        
        ip_json = json.loads(ip_request)
        
        os.system("clear")
        
        if ip_json["status"] != "success":
            print(f"{Fore.RED}[-]{Fore.WHITE} {Fore.GREEN}Error fetching IP data: {ip_json['message']} for query {ip_json['query']}! Please try again.{Fore.WHITE}")
            break
        
        print(f"{Fore.GREEN}[+] {Fore.GREEN}Showing results for {Fore.LIGHTGREEN_EX}{ip_json['query']}:")
        
        table = PrettyTable(["Key", "Value"])

        def safe_get(key):
            value = ip_json.get(key)
            if isinstance(value, bool):
                return "Yes" if value else "No"
            return value if value not in [None, ""] else "N/A"

        table.add_row(["Continent", f"{safe_get('continent')} ({safe_get('continentCode')})"])
        table.add_row(["Country", f"{safe_get('country')} ({safe_get('countryCode')})"])
        table.add_row(["Region", f"{safe_get('regionName')} ({safe_get('region')})"])
        table.add_row(["City", safe_get("city")])
        table.add_row(["Zip Code", safe_get("zip")])
        table.add_row(["Coordinates (lat, lon)", f"{safe_get('lat')}, {safe_get('lon')}"])
        table.add_row(["Timezone", safe_get("timezone")])
        table.add_row(["Internet Service Provider (ISP)", safe_get("isp")])
        table.add_row(["Organization (ORG)", safe_get("org")])
        table.add_row(["Autonomous System (AS)", safe_get("as")])
        table.add_row(["AS Name", safe_get("asname")])
        table.add_row(["Mobile Carrier Network", safe_get("mobile")])
        table.add_row(["Proxy Server", safe_get("proxy")])
        table.add_row(["Hosting", safe_get("hosting")])

        if ip_json.get("mobile") and ip_json.get("proxy") and ip_json.get("hosting"):
            using_vpn = "Most Likely"
        else:
            using_vpn = "Unlikely"
        table.add_row(["Virtual Private Network", using_vpn])

        table.add_row(["Currency", safe_get("currency")])
    
        print(fade.greenblue(str(table)))
        
        while True:
            
            commands = {
                "help": help,
                "new": new,
            }
            
            while True:
                console = input(f"{Fore.CYAN}[*] {Fore.GREEN}OrionLocator> ").strip().lower()
                if console == "exit":
                    break
                commands.get(console, unknown)()
            
    else: 
        print(f"{Fore.RED}[-]{Fore.WHITE} {Fore.GREEN}Invalid IP address format! Please try again.{Fore.WHITE}") 

