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
  async def _log_og(self, og: str, service_id: str):
    raise NotImplementedError()
  
  @abstractmethod
  async def _log_semi_og(self, semi_og: str, service_id: str):
    raise NotImplementedError()
  
  @abstractmethod
  async def _log_rate_limit(self, name: str, err: RateError, service_id: str):
    raise NotImplementedError()

  @abstractmethod
  async def _log_error(self, name: str, err, service_id: str):
    raise NotImplementedError()

  @abstractmethod
  async def log_og(self, og: str, service_id: str):
    try:
      await self._log_og(og, service_id)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_og(og, service_id)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
  
  @abstractmethod
  async def log_semi_og(self, semi_og: str, service_id: str):
    try:
      await self._log_semi_og(semi_og, service_id)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_semi_og(semi_og, service_id)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
  
  @abstractmethod
  async def log_rate_limit(self, name: str, err: RateError, service_id: str):
    try:
      await self._log_rate_limit(name, err, service_id)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_rate_limit(name, err, service_id)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)

  @abstractmethod
  async def log_error(self, name: str, err, service_id: str):
    try:
      await self._log_error(name, err, service_id)
    except RateError as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: flood wait for {e.time}")
      await asyncio.sleep(e.time + 1)
      return await self.log_error(name, err, service_id)
    except Exception as e:
      print(Fore.RED + f"[{self.get_id()} LOGGER]: unhandled err -> {e}" + Fore.RESET)
