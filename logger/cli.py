from errors.errors import RateError
from .logger import Logger
from colorama import Fore

class CliLogger(Logger):
  def __init__(self) -> None:
    super().__init__()

  def get_id(self) -> str:
    return "CLI"

  async def _log_og(self, og: str, service_id: str):
    print(Fore.GREEN + f"[{service_id}]: {og} is valid OG" + Fore.RESET)
  
  async def _log_semi_og(self, semi_og: str, service_id: str):
    print(Fore.YELLOW + f"[{service_id}]: {semi_og} is valid semi OG" + Fore.RESET)

  async def _log_rate_limit(self, name: str, err: RateError, service_id: str):
    print(Fore.RED + f"[{service_id}]: > the closest proxy rate limited for {err.time} secs, waiting" + Fore.RESET)

  async def _log_error(self, name: str, err, service_id: str):
    print(Fore.RED + f"[{service_id}]: > could not check name '{name}' -> {err}" + Fore.RESET)