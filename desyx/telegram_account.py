from .restrict import Restrictable

class TelegramAccount(Restrictable):
  def __init__(self, name: str, api_id: str, api_hash: str, phone_number: str, password: str):
    self.name = name
    self.api_id = api_id
    self.api_hash = api_hash
    self.phone_number = phone_number
    self.password = password
    super().__init__()

  @staticmethod
  def from_dict(dict) -> "TelegramAccount":
    return TelegramAccount(dict['session_name'], dict['api_id'], dict['api_hash'], dict['phone_number'], dict['2fa_pass'])