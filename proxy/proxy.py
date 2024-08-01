from restrict.restrict import Restrictable

class Proxy(Restrictable):
  def __init__(self, name: str, scheme: str, hostname: str, port: int, username: str | None = None, password: str | None = None, trusted: bool = False):
    self.name = name
    self.scheme = scheme
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password
    super().__init__(trusted, scheme != "http")

  @staticmethod
  def from_dict(dict) -> "Proxy":
    return Proxy(dict["name"], dict["scheme"], dict["hostname"], dict["port"], dict.get("username"), dict.get("password"), dict.get("trusted"))
  
  def get_proxy_as_url(self) -> dict | None:
    url = f"{self.scheme}://"
    if self.username is not None and self.password is not None:
      url += f"{self.username}:{self.password}@"
    url += f"{self.hostname}:{self.port}"

    return url
  
  def get_pyrogram_proxy(self) -> dict | None:
    return {
      "scheme": self.scheme,
      "hostname": self.hostname,
      "port": self.port,
      "username": self.username,
      "password": self.password
    }
  
  def __str__(self) -> str:
    return f"{self.name} x -> {self.get_restricted_till().strftime('%Y-%m-%d %H:%M:%S')}"

class NoProxy(Proxy):
  def __init__(self):
    super().__init__("<noproxy>", None, None, None, None, None, True)

  def get_proxy_as_url(self) -> dict | None:
    return None
  
  def get_pyrogram_proxy(self) -> dict | None:
    return None