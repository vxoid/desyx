from multiprocessing import Process
from .processes import Processes
from desyx.desyx import Desyx
from og.digitize import Digitize
from og.prefix import Prefix
from og.sufix import Sufix
from og.random import Random
from og.repeat import Repeat
from .service import Service
from og.og import Generator
from typing import List
import signal

OG_MUTS = [Repeat(amount=5), Random(amount=10)]
SEMI_MUTS = [Prefix(amount=3), Sufix(), Digitize(amount=1)]

def run_bot(gen: Generator, service: Service):
  bot = Desyx(gen, service)

  print(f"✅ {bot.service_name}")
  bot.run()

class Services(Processes):
  def __init__(self, services: List[Service]):
    if len(services) < 1:
      raise ValueError(f"No Services Provided")
    
    self.services = services
    super().__init__()

  def run_desyx_processes(self):
    signal.signal(signal.SIGINT, self.exit)
    generator = Generator()

    for service in self.services:
      process = Process(target=run_bot, name=service.get_name(), args=[generator, service])
      process.start()
      self.processes.append(process)

    for p in self.processes:
      p.join()
