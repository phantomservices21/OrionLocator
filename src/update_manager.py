from colorama import Fore
import config_manager
import requests_manager
import os
import subprocess


def canCheckForUpdates():
    check_for_updates = config_manager.readConfig("UPDATES", "check_for_updates")

    if check_for_updates == "null":
        while True:
            check = input(
                f"{Fore.CYAN}[*]{Fore.WHITE} Would you like to check for updates? {Fore.CYAN}[y/n]{Fore.WHITE} "
            ).lower()
            if check == "y":
                config_manager.writeConfig("UPDATES", "check_for_updates", "true")
                downloadUpdate()
                break
            elif check == "n":
                config_manager.writeConfig("UPDATES", "check_for_updates", "false")
                break
            else:
                print(f"{Fore.RED}[-]{Fore.WHITE} Invalid option! Please try again.")
    elif check_for_updates == "true":
        downloadUpdate()
    elif check_for_updates == "false":
        pass


# def isUpdateAvailable(current_version):
#     latest_version = requests_manager.get(
#         "https://raw.githubusercontent.com/phantomservices21/orionlocator/refs/heads/main/VERSION",
#     )

#     if current_version < float(latest_version):
#         while True:
#             proceed = input(
#                 f"{Fore.CYAN}[*]{Fore.WHITE} There is an update available ({current_version} -> {latest_version}). Would you like to update? {Fore.CYAN}[y/n]{Fore.WHITE} "
#             ).lower()
#             if proceed == "y":
#                 downloadUpdate()
#                 break
#             elif proceed == "n":
#                 break
#             else:
#                 print(f"{Fore.RED}[-]{Fore.WHITE} Invalid option! Please try again.")


def downloadUpdate():
    REPO_DIR = "../OrionLocator"

    os.system("cls")
    cwd = os.getcwd()
    os.chdir(REPO_DIR)

    subprocess.run(["git", "fetch"], check=True)
    result = subprocess.run(
        ["git", "rev-list", "HEAD...origin/main", "--count"],
        capture_output=True,
        text=True,
    )

    if result.stdout.strip() != "0":
        while True:
            proceed = input(
                f"{Fore.CYAN}[*]{Fore.WHITE} There is an update available. Would you like to update? {Fore.CYAN}[y/n]{Fore.WHITE} "
            ).lower()
            if proceed == "y":
                subprocess.run(["git", "reset", "--hard", "origin/main"], check=True)
                subprocess.run(["git", "clean", "-fd"], check=True)
                break
            elif proceed == "n":
                break
            else:
                print(f"{Fore.RED}[-]{Fore.WHITE} Invalid option! Please try again.")
    else:
        print(f"{Fore.GREEN}[+]{Fore.WHITE} Already up to date.")

    os.chdir(cwd)
