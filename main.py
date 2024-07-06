from desyx.services import Services
from desyx.discord import Discord
import config

if __name__ == '__main__':
  services = Services([Discord(proxies=config.proxies, useself=(len(config.proxies) < 1))])
  services.run_desyx_processes()