import json
import aiohttp
from errors.errors import *
from .service import Service
from proxy.proxy import Proxy
from proxy.proxies import Proxies

class Discord(Service):
  HEADERS = {
    "Content-Type": "application/json"
  }
  def __init__(self, proxies: Proxies):
    self.session = aiohttp.ClientSession(headers=Discord.HEADERS)
    super().__init__(proxies=proxies, min_len=2, max_len=10, trusted_only=False, secure_only=True)

  def get_id(self) -> str:
    return "discord"

  async def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

    proxiesdict = proxy.get_http_client_proxy()

    async with self.session.post(url, data=json.dumps({ "username": username }), proxy=proxiesdict) as response:
      response_json = await response.json()

      if "taken" not in response_json:
        if "retry_after" in response_json:
          raise RateError(response_json["retry_after"])
        
        if "message" not in response_json:
          raise UnknownError(f"couldn't parse the response -> {response_json}", -1)
        
        raise UnknownError(response_json["message"], response_json.get("errors"))

      return not response_json["taken"]
    
  async def close(self):
    await self.session.close()