from restrict.restrict import Restrictable

class TwitterAccount(Restrictable):
  def __init__(self, cookies: dict):
    self.__cookies = cookies
    super().__init__()
    
  def get_cookies(self):
    return self.__cookies

  @staticmethod
  def from_dict(dict) -> "TwitterAccount":
    return TwitterAccount(dict)