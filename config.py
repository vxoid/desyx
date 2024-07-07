import os
import json
from colorama import Fore
from desyx.proxy import Proxy
from desyx.account import Account
from dotenv import load_dotenv

load_dotenv()

proxies_file = os.getenv("PROXIES_FILE") or "proxies.json"
twitter_accounts_file = os.getenv("TWITTER_ACCOUNTS") or "twitter.json"

try:
  with open(proxies_file, 'r') as file:
    proxies = [Proxy.from_dict(proxy_dict) for proxy_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read proxies file `{proxies_file}` due to {e}" + Fore.RESET)
  proxies = []

try:
  with open(twitter_accounts_file, 'r') as file:
    twitter_accounts = [Account.from_dict(account_dict) for account_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read twitter accounts file `{twitter_accounts_file}` due to {e}" + Fore.RESET)
  twitter_accounts = []