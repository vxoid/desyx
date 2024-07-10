from datetime import datetime, timedelta
from typing import List

class Restrictable:
  def __init__(self):
    self.__restricted_till = datetime.now()
  
  def available(self) -> bool:
    cur_time = datetime.now()
    return cur_time >= self.__restricted_till

  def get_restricted_till(self):
    return self.__restricted_till

  def set_rate_limit(self, for_secs: float):
    self.__restricted_till = datetime.now() + timedelta(seconds=for_secs)

class RestrictableHolder:
  def __init__(self, restrictables: List[Restrictable]) -> None:
    self.restrictables = restrictables
    
  def _get_most_recently_unlocked(self) -> Restrictable:
    cur_time = datetime.now()
    result = self.restrictables[0]
    
    for proxy in self.restrictables:
      if proxy.get_restricted_till() - cur_time < result.get_restricted_till() - cur_time:
        result = proxy

    return result

  def _get_available(self) -> List[Restrictable]:
    return [restrictable for restrictable in self.restrictables if restrictable.available()]