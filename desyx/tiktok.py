import json
import requests
from .errors import *
from typing import List
from .proxy import Proxy, NoProxy
from .service import Service

class TikTok(Service):
  def __init__(self, proxies: List[Proxy] = [], useself: bool = True):
    super().__init__(proxies=proxies, useself=useself, min_len=2, max_len=10)

  def get_name(self) -> str:
    return "tiktok"

  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    url = ""

    proxies = None
    if type(proxy) is not NoProxy:
      proxies = {}
      http = proxy.get_http()
      if http is not None:
        proxies["http"] = http

      https = proxy.get_https()
      if https is not None:
        proxies["https"] = https