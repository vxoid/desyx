from logger.telegram_logger_profile import TelegramLoggerProfile
from aiogram.utils.markdown import hbold, hblockquote
from aiogram.exceptions import TelegramRetryAfter
from restrict.restrict import RestrictableHolder
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

  async def _log_og(self, og: str, service_id: str):
    await self.__log(f"[{service_id}]: '{hbold(og)}' is valid OG")
  
  async def _log_semi_og(self, semi_og: str, service_id: str):
    await self.__log(f"[{service_id}]: '{semi_og}' is valid semi OG")

  async def _log_rate_limit(self, name: str, err: RateError, service_id: str):
    await self.__log(f"[{service_id}]: > the closest proxy rate limited for {hbold(int(err.time))} secs, waiting to check {hbold(name)}")

  async def _log_error(self, name: str, err, service_id: str):
    await self.__log(f"[{service_id}]: > could not check name '{hbold(name)}' -> {hbold(err)}*")