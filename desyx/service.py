from .proxy import Proxy, NoProxy
from abc import abstractmethod
from datetime import datetime
from .errors import RateError
from typing import List
import random

USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.3',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.20',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.3',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15',
]

class Service:
  def __init__(self, proxies: List[Proxy] = [], useself: bool = True, min_len: int = 2, max_len: int = 10):
    if not useself and len(proxies) < 1:
      raise ValueError(f"no proxies provided while useself is False.")
    
    self.proxies = proxies
    if useself:
      self.proxies.append(NoProxy())
    self.useself = useself
    self.min_len = min_len
    self.max_len = max_len

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
      