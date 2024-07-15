from desyx.instagram import Instagram
from desyx.telegram import Telegram
from desyx.services import Services
from desyx.twitter import Twitter
from desyx.discord import Discord

if __name__ == '__main__':
  import config
  useself = len(config.proxies) < 1

  medias = []
  try:
    medias.append(Discord(proxies=config.proxies, useself=useself))
  except:
    pass
  try:
    medias.append(Instagram(proxies=config.proxies, useself=useself))
  except:
    pass
  try:
    medias.append(Telegram(accounts=config.telegram_accounts, proxies=config.proxies, useself=useself, session_dir=config.telegram_session_dir))
  except:
    pass

  if len(config.twitter_accounts) > 0:
    try:
      medias.append(Twitter(accounts=config.twitter_accounts, proxies=config.proxies, useself=useself))
    except:
      pass

  services = Services(medias)
  
  services.run_desyx_processes()