import random
import requests
from .errors import *
from typing import List
from .account import Account
from datetime import datetime
from .proxy import Proxy, NoProxy
from .service import Service, USER_AGENTS

class Twitter(Service):
  def __init__(self, accounts: List[Account], proxies: List[Proxy] = [], useself: bool = True):
    if len(accounts) < 1:
      raise ValueError(f"Twitter bot needs at least 1 account to live")
    
    self.accounts = accounts

    super().__init__(proxies=proxies, useself=useself, min_len=5, max_len=10)

  def get_name(self) -> str:
    return "twitter"
  
  def __get_available_accounts(self) -> List[Account]:
    return [account for account in self.accounts if account.available()]
  
  def __get_most_recently_unlocked_account(self) -> Account:
    cur_time = datetime.now()
    result = self.accounts[0]
    
    for account in self.accounts:
      if account.get_restricted_till() - cur_time < result.get_restricted_till() - cur_time:
        result = account

    return result

  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = f"https://x.com/i/api/i/users/username_available.json?suggest=false&username={username}"
    accounts = self.__get_available_accounts()
    if len(accounts) < 1:
      account = self.__get_most_recently_unlocked_account()
      raise RateError((account.get_restricted_till() - datetime.now()).total_seconds())

    account = random.choice(accounts)
    cookies = account.get_cookies()
    headers = {
      'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
      'cookie': '; '.join(f'{k}={v}' for k, v in cookies.items()),
      'referer': 'https://twitter.com/',
      'user-agent': random.choice(USER_AGENTS),
      'x-csrf-token': cookies.get('ct0', ''),
      'x-guest-token': cookies.get('guest_token', ''),
      'x-twitter-auth-type': 'OAuth2Session' if cookies.get('auth_token') else '',
      'x-twitter-active-user': 'yes',
      'x-twitter-client-language': 'en'
    }

    proxies = None
    if type(proxy) is not NoProxy:
      proxies = {}
      http = proxy.get_http()
      if http is not None:
        proxies["http"] = http

      https = proxy.get_https()
      if https is not None:
        proxies["https"] = https

    response = requests.get(url, headers=headers, proxies=proxies)
    try: 
      response_json = response.json()
      if "valid" not in response_json:      
        raise UnknownError(response.text, response_json.get("errors"))
    except Exception as e:
      raise UnknownError(response.text, [e])

    return response_json["valid"]