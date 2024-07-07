from datetime import datetime, timedelta

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