from restrict.restrict import Restrictable, RestrictableHolder
from errors.errors import RateError, UnknownError
from proxy.proxies import Proxies
from proxy.proxy import NoProxy
from abc import abstractmethod
from typing import List

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

class Service():
  def __init__(self, proxies: Proxies, min_len: int = 2, max_len: int = 10, trusted_only: bool = True, secure_only: bool = True):
    try:
      if trusted_only:
        proxies = proxies.filter_trusted()

      if secure_only:
        proxies = proxies.filter_secure()
    except ValueError as e:
      raise ValueError(f"[{self.get_id()}]: {e}")
    
    self.min_len = min_len
    self.max_len = max_len
    self.proxies = proxies
  
  @abstractmethod
  def get_id(self) -> str:
    raise NotImplementedError()
  
  @abstractmethod
  async def _unchecked_username_valid(self, username: str, proxy: Restrictable) -> bool:
    raise NotImplementedError()
    
  async def check_username_valid(self, username: str) -> bool:
    proxy = self.proxies._get_random()
    
    try:
      return await self._unchecked_username_valid(username, proxy)
    except RateError as re:
      proxy.set_rate_limit(re.time)
      return await self.check_username_valid(username)
    except UnknownError as e:
      raise e
    except Exception as e:
      proxy.set_rate_limit(UNEXPECTED_ERROR_WAIT)
      raise e
    
  async def close(self):
    pass