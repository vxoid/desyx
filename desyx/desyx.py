import time
from .errors import RateError
from .service import Service
from og.og import Generator
from colorama import Fore

class Desyx:
  def __init__(self, generator: Generator, service: Service, semi_muts = []):
    self.service = service
    self.service_name = service.get_name()
    self.generator = generator
    self.semi_muts = semi_muts
  
  def __print_prefix(self) -> str:
    return f"[{self.service_name}]: "

  def __handle_username(self, name: str, is_semi: bool = False) -> bool:
    prefix = self.__print_prefix()

    try:
      valid = self.service.check_username_valid(name)

      if valid:
        if is_semi:
          print(Fore.YELLOW + f"{prefix}'{name}' is valid semi OG" + Fore.RESET)
        else:
          print(Fore.GREEN + f"{prefix}'{name}' is valid OG" + Fore.RESET)

      return valid
    except RateError as err:
      self.__handle_rate_limit(err)
      time.sleep(err.time + 1)
      return self.__handle_username(name, is_semi)
    except Exception as err:
      self.__handle_error(name, err)
      return False  

  def __handle_error(self, name: str, err):
    prefix = self.__print_prefix()
    print(Fore.RED + f"{prefix}> could not check name '{name}' -> {err}" + Fore.RESET)

  def __handle_rate_limit(self, err):
    prefix = self.__print_prefix()
    print(Fore.RED + f"{prefix}> The closest proxy rate limited for {err.time} secs, waiting" + Fore.RESET)

  def run(self):
    while True:
      for name in self.generator.generate(min_length=self.service.min_len, max_length=self.service.max_len):
        if self.__handle_username(name.get_main()):
          continue

        for semi in name.get_semis(muts=self.semi_muts):
          self.__handle_username(semi, is_semi=True)