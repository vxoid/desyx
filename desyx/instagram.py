import re
import random
import requests
from .errors import *
from typing import List
from .proxy import Proxy
from .service import Service, USER_AGENTS

def get_ig_app_id():
  response = requests.get("https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/faada8fcb55f.js")
  return re.search("e\.instagramWebDesktopFBAppId='(.*?)'", response.text).group(1)

class Instagram(Service):
  def __init__(self, proxies: List[Proxy] = [], useself: bool = True):
    x_ig_app_id = get_ig_app_id()
    if x_ig_app_id is None:
      raise ValueError("could not fetch ig app id, this version needs an update")
    
    self.ig_app_id = x_ig_app_id
    super().__init__(proxies=proxies, useself=useself, min_len=1, max_len=10)

  def get_name(self) -> str:
    return "instagram"

  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    heeaders = {
      'user-agent': random.choice(USER_AGENTS),
      'X-Ig-App-Id': self.ig_app_id
    }

    proxies = proxy.get_requests_proxy()

    response = requests.get(url, headers=heeaders, proxies=proxies)
    if response.status_code == 404:
      return True
    elif response.status_code == 200:
      return False
    elif response.status_code == 429:
      raise RateError()
    
    raise UnknownError(f"Response status code is not 200, {response.status_code} -> {response.text}")