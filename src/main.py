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
from timezonefinder import TimezoneFinder
import datetime
import pytz
from geopy.distance import geodesic
import subprocess

tf = TimezoneFinder()

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
    while True:
        ip_addr = input(
            f"{Fore.CYAN}[*] {Fore.GREEN}Enter the IP Address (leave blank for your own):{Fore.WHITE} "
        ).strip()

        if ip_addr == "":
            skip_regex = True
        else:
            skip_regex = False

        if skip_regex or re.search(regex, ip_addr):
            ip_request = requests_manager.get(
                f"http://ip-api.com/json/{ip_addr}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
            )
            ip_json = json.loads(ip_request)

            os.system("cls")

            if ip_json["status"] != "success":
                print(
                    f"{Fore.RED}[-]{Fore.WHITE} {Fore.GREEN}Error fetching IP data: {ip_json['message']} for query {ip_json['query']}! Please try again.{Fore.WHITE}"
                )
                continue

            print(
                f"{Fore.GREEN}[+] {Fore.GREEN}Showing results for {Fore.LIGHTGREEN_EX}{ip_json['query']}:"
            )

            table = PrettyTable(["Key", "Value"])

            def safe_get(key):
                value = ip_json.get(key)
                if isinstance(value, bool):
                    return "Yes" if value else "No"
                return value if value not in [None, ""] else "N/A"

            table.add_row(
                ["Continent", f"{safe_get('continent')} ({safe_get('continentCode')})"]
            )
            table.add_row(
                ["Country", f"{safe_get('country')} ({safe_get('countryCode')})"]
            )
            table.add_row(
                ["Region", f"{safe_get('regionName')} ({safe_get('region')})"]
            )
            table.add_row(["City", safe_get("city")])
            table.add_row(["Zip Code", safe_get("zip")])
            table.add_row(
                ["Coordinates (lat, lon)", f"{safe_get('lat')}, {safe_get('lon')}"]
            )
            table.add_row(["Timezone", safe_get("timezone")])
            table.add_row(["Internet Service Provider (ISP)", safe_get("isp")])
            table.add_row(["Organization (ORG)", safe_get("org")])
            table.add_row(["Autonomous System (AS)", safe_get("as")])
            table.add_row(["AS Name", safe_get("asname")])
            table.add_row(["Mobile Carrier Network", safe_get("mobile")])
            table.add_row(["Proxy Server", safe_get("proxy")])
            table.add_row(["Hosting", safe_get("hosting")])
            if (
                ip_json.get("mobile")
                and ip_json.get("proxy")
                and ip_json.get("hosting")
            ):
                using_vpn = "Most Likely"
            else:
                using_vpn = "Unlikely"
            table.add_row(["Virtual Private Network", using_vpn])
            table.add_row(["Currency", safe_get("currency")])
            print(fade.greenblue(str(table)))
            break
        else:
            print(
                f"{Fore.RED}[-]{Fore.WHITE} {Fore.GREEN}Invalid IP address format! Please try again.{Fore.WHITE}"
            )

    # Command console loop
    while True:
        console = input(f"{Fore.CYAN}[*] {Fore.GREEN}OrionLocator> ").strip().lower()
        if console == "exit":
            exit()
        elif console == "help":
            print(
                f"""{Fore.LIGHTGREEN_EX}
Available Commands:

help         - Show this help message.
new          - Start a new IP address lookup.
map          - Open the IP's location in Google Maps using coordinates.
time         - Display the current local time at the IP's location.
distance     - Calculate the distance between your IP and the target IP.
ping         - Ping the target IP address (Ctrl+C to stop).
node-check   - Check if the IP is a known Tor exit node.
        {Fore.WHITE}"""
            )

        elif console == "new":
            break
        elif console == "map":
            map_url = (
                f"https://www.google.com/maps/place/{safe_get("lat")},{safe_get("lon")}"
            )
            os.system(f"start {map_url}")
            print(
                f"Your browser should have automatically opened Google Maps. If not you can manually open this link.\n{map_url}"
            )
        elif console == "time":
            timezone_str = tf.timezone_at(lng=safe_get("lon"), lat=safe_get("lat"))
            if timezone_str:
                timezone = pytz.timezone(timezone_str)
                current_time = datetime.datetime.now(timezone)
                print(current_time.strftime("%m/%d/%Y %I:%M%p"))
            else:
                print("Could not determine timezone for the given coordinates.")
        elif console == "distance":

            user_json = json.loads(
                requests_manager.get(
                    "http://ip-api.com/json/?fields=status,message,lat,lon"
                )
            )
            input_lat = float(safe_get("lat"))
            input_lon = float(safe_get("lon"))

            user_coords = (float(user_json["lat"]), float(user_json["lon"]))
            input_coords = (float(input_lat), float(input_lon))

            distance = geodesic(user_coords, input_coords).miles
            km = distance * 1.60934
            print(f"Distance: {distance:.2f} miles ({km:.2f} kilometers)")
        elif console == "ping":
            try:
                print(f"Pinging {safe_get('query')}... Press Ctrl+C to stop.\n")
                subprocess.run(["ping", safe_get("query")])
            except KeyboardInterrupt:
                print("\nPing stopped.")
        elif console == "node-check":
            exit_nodes = requests_manager.get(
                "https://check.torproject.org/exit-addresses"
            )
            if safe_get("query") in exit_nodes:
                print("This IP os a known Tor exit node.")
            else:
                print("This IP is not a known Tor exit node.")
