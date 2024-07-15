from .restrict import Restrictable, RestrictableHolder
from .errors import RateError, UnknownError
from abc import abstractmethod
from datetime import datetime
from .proxy import NoProxy
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

UNEXPECTED_ERROR_WAIT = RateError().time

class Service(RestrictableHolder):
  def __init__(self, proxies: List[Restrictable] = [], useself: bool = True, min_len: int = 2, max_len: int = 10, trusted_only: bool = True, secure_only: bool = True):
    if trusted_only:
      proxies = [proxy for proxy in proxies if proxy.is_trusted()]

    if secure_only:
      proxies = [proxy for proxy in proxies if proxy.is_secure()]

    if not useself and len(proxies) < 1:
      raise ValueError(f"no valid proxies provided for {self.get_name()}, while useself is False.")
    
    self.useself = useself
    self.min_len = min_len
    self.max_len = max_len
    super().__init__(proxies)
    if useself:
      self.restrictables.append(NoProxy())
    
  @abstractmethod
  def get_name(self) -> str:
    raise NotImplementedError()
  
  @abstractmethod
  def _unchecked_username_valid(self, username: str, proxy: Restrictable) -> bool:
    raise NotImplementedError()
    
  def check_username_valid(self, username: str) -> bool:
    proxy = self._get_random()
    
    try:
      return self._unchecked_username_valid(username, proxy)
    except RateError as re:
      proxy.set_rate_limit(re.time)
      return self.check_username_valid(username)
    except UnknownError as e:
      raise e
    except Exception as e:
      proxy.set_rate_limit(UNEXPECTED_ERROR_WAIT)
      raise e