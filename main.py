from desyx.instagram import Instagram
from desyx.twitter import Twitter
from desyx.services import Services
from desyx.discord import Discord
import config

if __name__ == '__main__':
  useself = len(config.proxies) < 1

  medias = [
    Discord(proxies=config.proxies, useself=useself),
    # Instagram(proxies=config.proxies, useself=useself)
  ]
  if len(config.twitter_accounts) > 0:
    medias.append(Twitter(accounts=config.twitter_accounts, proxies=config.proxies, useself=useself))

  services = Services(medias)
  
  services.run_desyx_processes()