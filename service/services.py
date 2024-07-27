from logger.logger import Logger
from desyx.desyx import Desyx
from og.digitize import Digitize
from og.prefix import Prefix
from og.sufix import Sufix
from og.random import Random
from og.repeat import Repeat
from .service import Service
from og.og import Generator
from typing import List
import asyncio

OG_MUTS = [Repeat(amount=5), Random(amount=10)]
SEMI_MUTS = []
SEMI_MUTS = [Prefix(amount=2), Sufix(), Digitize(amount=1)]

class Services:
  def __init__(self, services: List[Service], loggers: List[Logger]):
    if len(services) < 1:
      raise ValueError(f"No Services Provided")
    
    self.loggers = loggers
    self.services = services

  async def run_desyx_processes(self):
    generator = Generator(OG_MUTS)

    async with asyncio.TaskGroup() as tg:
      for service in self.services:
        bot = Desyx(generator, service, self.loggers, SEMI_MUTS)

        print(f"✅ {bot.service.get_id()}")
        tg.create_task(bot.run())