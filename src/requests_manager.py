import requests
from colorama import Fore


def get(
    url: str,
    params=None,
    allow_redirects: bool = None,
    auth=None,
    cert=None,
    cookies=None,
    headers=None,
    proxies=None,
    stream=False,
    timeout=None,
    verify=None,
    return_response: bool = False,
):
    try:
        response = requests.get(
            url=url,
            params=params,
            allow_redirects=allow_redirects,
            auth=auth,
            cert=cert,
            cookies=cookies,
            headers=headers,
            proxies=proxies,
            stream=stream,
            timeout=timeout,
            verify=verify,
        )
        if return_response:
            # Optionally, you can do response.raise_for_status() here if you want to handle errors immediately
            return response
        else:
            return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-]{Fore.WHITE} Request failed with error {e}.")
    except Exception as e:
        print(f"{Fore.RED}[-]{Fore.WHITE} Unknown error {e} occurred.")


def post(url: str, data: dict):
    try:
        requests.post(url, json=data).raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-]{Fore.WHITE} Request failed with error {e}.")
    except Exception as e:
        print(f"{Fore.RED}[-]{Fore.WHITE} Unknown error {e} occurred.")
