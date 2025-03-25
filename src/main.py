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
    ip_addr = input(f"{Fore.CYAN}[*]{Fore.WHITE} {Fore.GREEN}Enter the IP Address:{Fore.WHITE} ")

    regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

    if re.search(regex, ip_addr): 
        ip_request = requests_manager.get(f"http://ip-api.com/json/{ip_addr}")
        
        ip_json = json.loads(ip_request)
        
        os.system("clear")
        
        print(f"{Fore.GREEN}[+]{Fore.WHITE} {Fore.GREEN}Showing results for {Fore.LIGHTGREEN_EX}{ip_addr}:")
        
        table = PrettyTable(["Key", "Value"])

        # Add rows to the table
        table.add_row(["Country", f"{ip_json['country']} ({ip_json['countryCode']})"])
        table.add_row(["Region", f"{ip_json['regionName']} ({ip_json['region']})"])
        table.add_row(["City", ip_json["city"]])
        table.add_row(["Zip Code", ip_json["zip"]])
        table.add_row(["Coordinates (lat, lon)",f"{ip_json['lat']}, {ip_json['lon']}"])
        table.add_row(["Timezone", ip_json["timezone"]])
        table.add_row(["Internet Service Provider (ISP)", ip_json["isp"]])
        table.add_row(["Organization (ORG)", ip_json["org"]])
        table.add_row(["Autonomous System (AS)", ip_json["as"]])
    
        print(fade.greenblue(str(table)))
        
        # TODO: Finish console to add extra commands.
            
    else: 
        print(f"{Fore.RED}[-]{Fore.WHITE} {Fore.GREEN}Invalid IP address format! Please try again.{Fore.WHITE}") 

