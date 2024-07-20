from typing import List
from .proxy import Proxy
from restrict.restrict import RestrictableHolder

class Proxies(RestrictableHolder):
  def __init__(self, proxies: List[Proxy] = []):
    if len(proxies) < 1:
      raise ValueError(f"no valid proxies provided.")
    super().__init__(proxies)

  def filter_trusted(self) -> "Proxies":
    return Proxies([restrictable for restrictable in self.restrictables if restrictable.is_trusted()])

  def filter_secure(self) -> "Proxies":
    return Proxies([restrictable for restrictable in self.restrictables if restrictable.is_secure()])