from colorama import Fore
import config_manager
import requests_manager
import os
import subprocess
import shutil


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
    CONFIG_REL_PATH = os.path.join("src", "cfg", "config.ini")
    config_path = os.path.join(REPO_DIR, CONFIG_REL_PATH)
    backup_path = config_path + ".bak"

    # Back up the user-specific config file if it exists
    if os.path.exists(config_path):
        shutil.copy2(config_path, backup_path)
        print(f"{Fore.YELLOW}[!]{Fore.WHITE} Backed up {CONFIG_REL_PATH}.")

    # Ensure we're in the repository directory and that it's a Git repo
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        subprocess.run(["git", "init"], check=True, cwd=REPO_DIR)

    # Ensure remote 'origin' is set correctly
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=REPO_DIR,
            check=True,
        )
        existing_url = result.stdout.strip()
        if existing_url != "https://github.com/phantomservices21/OrionLocator.git":
            print(f"{Fore.YELLOW}[!]{Fore.WHITE} Updating remote URL for 'origin'.")
            subprocess.run(
                [
                    "git",
                    "remote",
                    "set-url",
                    "origin",
                    "https://github.com/phantomservices21/OrionLocator.git",
                ],
                check=True,
                cwd=REPO_DIR,
            )
    except subprocess.CalledProcessError:
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "https://github.com/phantomservices21/OrionLocator.git",
            ],
            check=True,
            cwd=REPO_DIR,
        )

    # Clear the screen and change to the repo directory
    os.system("cls")
    cwd = os.getcwd()
    os.chdir(REPO_DIR)

    # Fetch updates from the remote repository
    subprocess.run(["git", "fetch"], check=True)
    result = subprocess.run(
        ["git", "rev-list", "HEAD...origin/main", "--count"],
        capture_output=True,
        text=True,
        check=True,
    )

    # If there's an update available, prompt the user to update
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

    # Change back to the original working directory
    os.chdir(cwd)

    # Restore the user-specific config file from backup, if it was backed up
    if os.path.exists(backup_path):
        shutil.move(backup_path, config_path)
        print(f"{Fore.GREEN}[+]{Fore.WHITE} Restored user config at {CONFIG_REL_PATH}.")
