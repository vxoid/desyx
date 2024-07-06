from datetime import datetime, timedelta
from .proxy import Proxy, NoProxy
from abc import abstractmethod
from .errors import RateError
from typing import List
import random

class Service:
  def __init__(self, proxies: List[Proxy] = [], useself: bool = True):
    if not useself and len(proxies) < 1:
      raise ValueError(f"no proxies provided while useself is False.")
    
    self.proxies = proxies
    if useself:
      self.proxies.append(NoProxy())
    self.useself = useself

  @abstractmethod
  def get_name(self) -> str:
    raise NotImplementedError()
  
  @abstractmethod
  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    raise NotImplementedError()
    
  def check_username_valid(self, username: str) -> bool:
    available = self.__get_available_proxies()
    if len(available) < 1:
      proxy = self.__get_most_recently_unlocked_proxy()
      raise RateError((proxy.get_restricted_till() - datetime.now()).total_seconds())
    
    proxy = random.choice(available)
    try:
      return self._unchecked_username_valid(username, proxy)
    except RateError as re:
      proxy.set_rate_limit(re.time)
      return self.check_username_valid(username)
    except Exception as e:
      raise e

  def __get_most_recently_unlocked_proxy(self) -> Proxy:
    cur_time = datetime.now()
    result = self.proxies[0]
    
    for proxy in self.proxies:
      if proxy.get_restricted_till() - cur_time < result.get_restricted_till() - cur_time:
        result = proxy

    return result

  def __get_available_proxies(self) -> List[Proxy]:
    return [proxy for proxy in self.proxies if proxy.available()]
      