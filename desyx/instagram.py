import json
import requests
from .errors import *
from typing import List
from .proxy import Proxy, NoProxy
from .service import Service

class Instagram(Service):
  def __init__(self, proxies: List[Proxy] = [], useself: bool = True):
    super().__init__(proxies=proxies, useself=useself, min_len=1, max_len=10)

  def get_name(self) -> str:
    return "instagram"

  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    return False