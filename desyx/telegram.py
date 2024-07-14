from .errors import *
from typing import List
from .proxy import Proxy
from pyrogram import Client
from .restrict import RestrictableHolder
from .telegram_account import TelegramAccount
from pyrogram.errors import UsernameNotOccupied
from .service import Service, UNEXPECTED_ERROR_WAIT

class Telegram(Service):
  def __init__(self, accounts: List[TelegramAccount], proxies: List[Proxy] = [], useself: bool = True, session_dir: str = "sessions"):
    if len(accounts) < 1:
      raise ValueError(f"Telegram bot needs at least 1 account to live")
    
    self.session_dir = session_dir
    self.accounts = RestrictableHolder(accounts)
    super().__init__(proxies=proxies, useself=useself, min_len=5, max_len=10)

  def get_name(self) -> str:
    return "telegram"

  def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    account = self.accounts._get_random()
    proxies = proxy.get_pyrogram_proxy()

    client = Client(account.name, account.api_id, account.api_hash, workdir=self.session_dir, proxy=proxies)
    try:
      with client:
        try:
          client.resolve_peer(username)
          return False
        except UsernameNotOccupied:
          return True
    except ConnectionError as err:
      raise err