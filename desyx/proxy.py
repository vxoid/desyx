from .restrict import Restrictable

class Proxy(Restrictable):
  def __init__(self, name: str, http: str | None = None, https: str | None = None):
    self.__name = name
    self.__http = http
    self.__https = https
    super().__init__()

  @staticmethod
  def from_dict(dict) -> "Proxy":
    return Proxy(dict["name"], dict.get("http"), dict.get("https"))
  
  def get_name(self):
    return self.__name

  def get_http(self):
    return self.__http

  def get_https(self):
    return self.__https
  
  def __str__(self) -> str:
    return f"{self.__name} x -> {self.get_restricted_till().strftime('%Y-%m-%d %H:%M:%S')}"
  
class NoProxy(Proxy):
  def __init__(self):
    super().__init__("<noproxy>", None, None)