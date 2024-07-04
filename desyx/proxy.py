class Proxy:
  def __init__(self, name: str, http: str, https: str | None = None):
    self.name = name
    self.http = http
    self.https = https
  
  @staticmethod
  def from_dict(dict) -> "Proxy":
    return Proxy(dict["name"], dict["http"], dict.get("https"))