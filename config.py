import os
import json
from colorama import Fore
from proxy.proxy import Proxy
from dotenv import load_dotenv
from service.twitter_account import TwitterAccount
from service.telegram_account import TelegramAccount
from logger.telegram_logger_profile import TelegramLoggerProfile

load_dotenv()

proxies_file = os.getenv("PROXIES_FILE") or "proxies.json"
twitter_accounts_file = os.getenv("TWITTER_ACCOUNTS") or "twitter_accounts.json"
telegram_loggers_file = os.getenv("TELEGRAM_LOGGERS") or "telegram_loggers.json"
telegram_accounts_file = os.getenv("TELEGRAM_ACCOUNTS") or "telegram_accounts.json"
telegram_session_dir = os.getenv("TELEGRAM_SESSION_DIR")

try:
  with open(proxies_file, 'r') as file:
    proxies = [Proxy.from_dict(proxy_dict) for proxy_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read proxies file `{proxies_file}` due to {e}" + Fore.RESET)
  proxies = []

try:
  with open(twitter_accounts_file, 'r') as file:
    twitter_accounts = [TwitterAccount.from_dict(account_dict) for account_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read twitter accounts file `{twitter_accounts_file}` due to {e}" + Fore.RESET)
  twitter_accounts = []

try:
  with open(telegram_loggers_file, 'r') as file:
    telegram_loggers = [TelegramLoggerProfile.from_dict(telegram_logger_dict) for telegram_logger_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read telegram loggers file `{telegram_loggers_file}` due to {e}" + Fore.RESET)
  telegram_loggers = []

try:
  with open(telegram_accounts_file, 'r') as file:
    telegram_accounts = [TelegramAccount.from_dict(account_dict) for account_dict in json.load(file)]
except Exception as e:
  print(Fore.YELLOW + f"WARNING: couldn't read telegram accounts file `{telegram_accounts_file}` due to {e}" + Fore.RESET)
  telegram_accounts = []