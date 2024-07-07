from .restrict import Restrictable

class Account(Restrictable):
  def __init__(self, cookies: dict):
    self.__cookies = cookies
    super().__init__()
    
  def get_cookies(self):
    return self.__cookies

  @staticmethod
  def from_dict(dict) -> "Account":
    return Account(dict)