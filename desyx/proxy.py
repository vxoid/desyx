from datetime import datetime, timedelta



class Proxy:
  def __init__(self, name: str, http: str | None = None, https: str | None = None):
    self.__name = name
    self.__http = http
    self.__https = https
    self.__restricted_till = datetime.now()

  @staticmethod
  def from_dict(dict) -> "Proxy":
    return Proxy(dict["name"], dict.get("http"), dict.get("https"))
  
  def available(self) -> bool:
    cur_time = datetime.now()
    return cur_time >= self.__restricted_till
  
  def get_restricted_till(self):
    return self.__restricted_till
  
  def set_rate_limit(self, for_secs: float):
    self.__restricted_till = datetime.now() + timedelta(seconds=for_secs)
  
  def get_name(self):
    return self.__name

  def get_http(self):
    return self.__http

  def get_https(self):
    return self.__https
  
  def __str__(self) -> str:
    return f"{self.__name} x -> {self.__restricted_till.strftime('%Y-%m-%d %H:%M:%S')}"
  
class NoProxy(Proxy):
  def __init__(self):
    super().__init__("<noproxy>", None, None)