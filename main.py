from logger.telegram import TelegramLogger
from service.instagram import Instagram
from proxy.proxy import Proxy, NoProxy
from service.telegram import Telegram
from service.services import Services
from service.service import Service
from service.twitter import Twitter
from service.discord import Discord
from proxy.proxies import Proxies
from logger.cli import CliLogger
from colorama import Fore
import asyncio
import config
import copy

async def get_media():
  if len(config.proxies) < 1:
    config.proxies.append(NoProxy())

  try:
    yield Discord(Proxies(copy.deepcopy(config.proxies)))
  except Exception as e:
    print(Fore.YELLOW + e + Fore.RESET)
  try:
    yield await (Instagram.setup(Proxies(copy.deepcopy(config.proxies))))
  except Exception as e:
    print(Fore.YELLOW + e + Fore.RESET)
  try:
    yield Telegram(accounts=config.telegram_accounts, proxies=Proxies(copy.deepcopy(config.proxies)), session_dir=config.telegram_session_dir)
  except Exception as e:
    print(Fore.YELLOW + e + Fore.RESET)

  if len(config.twitter_accounts) > 0:
    try:
      yield Twitter(accounts=config.twitter_accounts, proxies=Proxies(copy.deepcopy(config.proxies)))
    except Exception as e:
      print(Fore.YELLOW + e + Fore.RESET)

async def main():
  medias = []
  try:
    async for media in get_media():
      medias.append(media)
    
    loggers = [CliLogger()]
    if len(config.telegram_loggers_file) > 0:
      loggers.append(TelegramLogger(config.telegram_loggers))

    services = Services(medias, loggers)
    
    await services.run_desyx_processes()
  finally:
    async with asyncio.TaskGroup() as tg:
      for media in medias:
        tg.create_task(media.close())

if __name__ == '__main__':
  asyncio.run(main())