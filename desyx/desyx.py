from errors.errors import RateError
from logger.logger import Logger
from logger.cli import CliLogger
from service.service import Service
from og.og import Generator
from typing import List
from og.mut import Mut
import asyncio
import time

class Desyx:
  def __init__(self, generator: Generator, service: Service, loggers: List[Logger] = [CliLogger()], semi_muts: List[Mut] = []):
    self.service = service
    self.service_id = service.get_id()
    self.generator = generator
    self.loggers = loggers
    self.semi_muts = semi_muts

  async def __handle_username(self, name: str, is_semi: bool = False) -> bool:
    async with asyncio.TaskGroup() as tg:
      try:
        valid = await self.service.check_username_valid(name)

        if valid:
          if is_semi:
            for logger in self.loggers:
              tg.create_task(logger.log_semi_og(name, self.service_id))
          else:
            for logger in self.loggers:
              tg.create_task(logger.log_og(name, self.service_id))

        return valid
      except RateError as err:
        tg.create_task(self.__handle_rate_limit(name, err))
        await asyncio.sleep(err.time + 1)
        return await self.__handle_username(name, is_semi)
      except Exception as err:
        tg.create_task(self.__handle_error(name, err))
        return False  

  async def __handle_error(self, name: str, err):
    for logger in self.loggers:
      await logger.log_error(name, err, self.service_id)

  async def __handle_rate_limit(self, name: str, err):
    for logger in self.loggers:
      await logger.log_rate_limit(name, err, self.service_id)

  async def run(self):
    while True:
      for name in self.generator.generate(min_length=self.service.min_len, max_length=self.service.max_len):
        if await self.__handle_username(name.get_main()):
          continue
        
        for semi in name.get_semis(muts=self.semi_muts):
          await self.__handle_username(semi, is_semi=True)