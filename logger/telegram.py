from logger.telegram_logger_profile import TelegramLoggerProfile
from aiogram.utils.markdown import hbold, hlink
from aiogram.exceptions import TelegramRetryAfter
from restrict.restrict import RestrictableHolder
from service.service import Service
from errors.errors import RateError
from .logger import Logger
from typing import List
import aiogram

class TelegramLogger(Logger):
  def __init__(self, profiles: List[TelegramLoggerProfile] = []):
    self.profiles = RestrictableHolder(profiles)
    super().__init__()

  def get_id(self) -> str:
    return "telegram"

  async def __log(self, message: str):
    profile = self.profiles._get_random()

    bot = aiogram.Bot(profile.token)
    try:
      await bot.send_message(profile.chat_id, message, parse_mode='HTML')
    except TelegramRetryAfter as e:
      profile.set_rate_limit(e.retry_after)
      return await self.__log(message)
    finally:
      await bot.session.close()

  async def _log_og(self, og: str, service: Service):
    await self.__log(f"[{service.get_id()}]: '{hlink(og, service.get_link(og)) or hbold(og)}' is valid OG")
  
  async def _log_semi_og(self, semi_og: str, service: Service):
    await self.__log(f"[{service.get_id()}]: '{hlink(semi_og, service.get_link(semi_og)) or semi_og}' is valid semi OG")
    # pass # ingore semis

  async def _log_rate_limit(self, name: str, err: RateError, service: Service):
    await self.__log(f"[{service.get_id()}]: > the closest proxy rate limited for {hbold(int(err.time))} secs, waiting to check {hlink(name, service.get_link(name)) or hbold(name)}")

  async def _log_error(self, name: str, err, service: Service):
    await self.__log(f"[{service.get_id()}]: > could not check name '{hlink(name, service.get_link(name)) or hbold(name)}' -> {hbold(err)}*")