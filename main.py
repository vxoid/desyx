import config
import sys, signal
from og.og import Generator
from desyx.desyx import Desyx
from desyx.proxy import Proxy
from multiprocessing import Process

def run_bot(gen: Generator, proxy: Proxy | None = None):
  bot = Desyx(gen, proxy)

  print(f"✅ {proxy.name if proxy is not None else '<no proxy>'}")
  bot.run()

def exit(signum, frame):
  print("Bye 👋")
  for p in processes:
    p.kill()
  sys.exit(0)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, exit)
  generator = Generator()

  processes = []

  for proxy in config.proxies:
    process = Process(target=run_bot, name=proxy.name, args=[generator, proxy])
    process.start()
    processes.append(process)

  for p in processes:
    p.join()