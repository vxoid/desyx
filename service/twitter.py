import random
import aiohttp
from typing import List
from proxy.proxy import Proxy
from proxy.proxies import Proxies
from errors.errors import *
from restrict.restrict import RestrictableHolder
from .service import Service, USER_AGENTS
from .twitter_account import TwitterAccount

class Twitter(Service):
  def __init__(self, accounts: List[TwitterAccount], proxies: Proxies):
    if len(accounts) < 1:
      raise ValueError(f"Twitter bot needs at least 1 account to live")
    
    self.session = aiohttp.ClientSession()
    self.accounts = RestrictableHolder(accounts)

    super().__init__(proxies=proxies, min_len=5, max_len=10, trusted_only=True, secure_only=True)

  def get_id(self) -> str:
    return "twitter"
  
  def get_link(self, username: str) -> str | None:
    return f"https://x.com/{username}"
  
  async def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = f"https://x.com/i/api/i/users/username_available.json?suggest=false&username={username}"
    
    account = self.accounts._get_random()
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

    proxydict = proxy.get_proxy_as_url()

    async with self.session.get(url, headers=headers, proxy=proxydict) as response:
      response_text = await response.text()
      if response_text == "":
        raise ValueError(f"response is empty")

      try: 
        response_json = await response.json()
        if "valid" not in response_json:      
          raise UnknownError(response_text, response_json.get("errors"))
      except Exception as e:
        raise UnknownError(response_text, [e])

      return response_json["valid"]
  
  async def close(self):
    await self.session.close()