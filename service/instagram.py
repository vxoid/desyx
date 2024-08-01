import re
import random
import aiohttp
from errors.errors import *
from proxy.proxy import Proxy
from proxy.proxies import Proxies
from .service import Service, USER_AGENTS

async def get_ig_app_id() -> str:
  async with aiohttp.ClientSession() as session:
    async with session.get("https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/faada8fcb55f.js") as response:
      return re.search("e\.instagramWebDesktopFBAppId='(.*?)'", await response.text()).group(1)

class Instagram(Service):
  @staticmethod
  async def setup(proxies: Proxies) -> "Instagram":
    return Instagram(await get_ig_app_id(), proxies)

  def __init__(self, x_ig_app_id: str, proxies: Proxies):    
    self.ig_app_id = x_ig_app_id
    print(f"IG app id: {self.ig_app_id}")
    self.session = aiohttp.ClientSession()
    super().__init__(proxies=proxies, min_len=1, max_len=10, trusted_only=False, secure_only=False)

  def get_id(self) -> str:
    return "instagram"

  def get_link(self, username: str) -> str | None:
    return f"https://www.instagram.com/{username}"

  async def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = f"http://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    headers = {
      'user-agent': random.choice(USER_AGENTS),
      'X-Ig-App-Id': self.ig_app_id
    }

    proxydict = proxy.get_proxy_as_url()
    if proxydict is None or "https" in proxydict:
      url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
    async with self.session.get(url, headers=headers, proxy=proxydict) as response:
      status = response.status
      if status == 404:
        return True
      elif status == 200:
        return False
      elif status == 429:
        raise RateError()
      
      raise UnknownError(f"Response status code is not 200, {status} -> {await response.text}")

  async def close(self):
    await self.session.close()