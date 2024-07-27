from service.service import Service
from errors.errors import RateError
from abc import abstractmethod
from colorama import Fore
import asyncio

class Logger:
  def __init__(self) -> None:
    pass 

  @abstractmethod
  def get_id(self) -> str:
    raise NotImplementedError()

  @abstractmethod
  async def _log_og(self, og: str, service: Service):
    raise NotImplementedError()
  
  @abstractmethod
  async def _log_semi_og(self, semi_og: str, service: Service):
    raise NotImplementedError()
  
  @abstractmethod
  async def _log_rate_limit(self, name: str, err: RateError, service: Service):
    raise NotImplementedError()

  @abstractmethod
  async def _log_error(self, name: str, err, service: Service):
    raise NotImplementedError()

  async def log_og(self, og: str, service: Service):
    try:
      await self._log_og(og, service)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_og(og, service)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
  
  async def log_semi_og(self, semi_og: str, service: Service):
    try:
      await self._log_semi_og(semi_og, service)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_semi_og(semi_og, service)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
  
  async def log_rate_limit(self, name: str, err: RateError, service: Service):
    try:
      await self._log_rate_limit(name, err, service)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_rate_limit(name, err, service)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
  
  async def log_error(self, name: str, err, service: Service):
    try:
      await self._log_error(name, err, service)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_error(name, err, service)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
