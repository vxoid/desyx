from typing import List
from proxy.proxy import Proxy
from errors.errors import *
from pyrogram import Client
from proxy.proxies import Proxies
from .service import Service
from restrict.restrict import RestrictableHolder
from .telegram_account import TelegramAccount
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid

class Telegram(Service):
  def __init__(self, accounts: List[TelegramAccount], proxies: Proxies, session_dir: str = "sessions"):
    if len(accounts) < 1:
      raise ValueError(f"Telegram bot needs at least 1 account to live")
    
    self.session_dir = session_dir
    self.accounts = RestrictableHolder(accounts)
    super().__init__(proxies=proxies, min_len=5, max_len=10, trusted_only=True, secure_only=True)

  def get_id(self) -> str:
    return "telegram"

  async def _unchecked_username_valid(self, username: str, proxy: Proxy) -> bool:
    account = self.accounts._get_random()
    proxies = proxy.get_pyrogram_proxy()

    client = Client(account.name, account.api_id, account.api_hash, workdir=self.session_dir, proxy=proxies)
    try:
      async with client:
        try:
          peer = await client.resolve_peer(username)
          return False
        except UsernameNotOccupied:
          return True
        except UsernameInvalid:
          return False
        except KeyError:
          return False
    except ConnectionError as err:
      raise err