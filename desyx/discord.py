import json
import requests
from .errors import *
from typing import List
from .proxy import Proxy
from .service import Service

class Discord(Service):
  HEADERS = {
    "Content-Type": "application/json"
  }
  def __init__(self, proxies: List[Proxy] = [], useself: bool = True):
    super().__init__(proxies=proxies, useself=useself, min_len=2, max_len=10, trusted_only=False, secure_only=True)

  def get_name(self) -> str:
    return "discord"

  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

    proxies = proxy.get_requests_proxy()
    
    response = requests.post(url, json.dumps({ "username": username }), headers=Discord.HEADERS, proxies=proxies)
    response_json = response.json()
    if "taken" not in response_json:
      if "retry_after" in response_json:
        raise RateError(response_json["retry_after"])
      
      if "message" not in response_json:
        raise UnknownError(f"couldn't parse the response -> {response_json}", -1)
      
      raise UnknownError(response_json["message"], response_json.get("errors"))

    return not response_json["taken"]