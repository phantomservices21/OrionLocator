current_version = 1.0

import os
from update_manager import canCheckForUpdates
import fade
from colorama import Fore

canCheckForUpdates()

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

input()
