import os
import json
from colorama import Fore
from desyx.proxy import Proxy
from dotenv import load_dotenv

load_dotenv()

proxies_file = os.getenv("PROXIES_FILE") or "proxies.json"

try:
  with open(proxies_file, 'r') as file:
    proxies = [Proxy.from_dict(proxy_dict) for proxy_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read proxies file `{proxies_file}` due to {e}" + Fore.RESET)
  proxies = []