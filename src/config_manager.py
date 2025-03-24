import configparser
from colorama import Fore

config = configparser.ConfigParser()

config.read("src/cfg/config.ini")


def readConfig(section, key):
    try:
        return config.get(section, key)
    except configparser.NoSectionError:
        print(f'{Fore.RED}[-]{Fore.WHITE} Section "{section}" not found.')
    except configparser.NoOptionError:
        print(
            f'{Fore.RED}[-]{Fore.WHITE} Key "{key}" not found in section "{section}".'
        )
    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Fore.WHITE} File not found.")


def writeConfig(section, key, value):
    try:
        config.set(section, key, value)
    except configparser.NoSectionError:
        print(f'{Fore.RED}[-]{Fore.WHITE} Section "{section}" not found.')
    except configparser.NoOptionError:
        print(
            f'{Fore.RED}[-]{Fore.WHITE} Key "{key}" not found in section "{section}".'
        )
    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Fore.WHITE} File not found.")

    with open("src/cfg/config.ini", "w") as configfile:
        config.write(configfile)
