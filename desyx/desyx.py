import time
import json
import requests
from og.repeat import Repeat
from og.prefix import Prefix
from og.sufix import Sufix
from og.digitize import Digitize
from .errors import *
from .proxy import Proxy
from colorama import Fore
from og.og import Generator

class Desyx:
  def __init__(self, generator: Generator, proxy: Proxy | None = None):
    self.proxy = proxy
    self.generator = generator

  def check_username_valid(self, username: str) -> bool:
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
    headers = {
      "Content-Type": "application/json"
    }

    proxies = None
    if self.proxy is not None:
      proxies = {
        "http": self.proxy.http,
      }
      if self.proxy.https is not None:
        proxies["https"] = self.proxy.https

    response = requests.post(url, json.dumps({ "username": username }), headers=headers, proxies=proxies)
    response_json = response.json()
    if "taken" not in response_json:
      if "retry_after" in response_json:
        raise RateError(response_json["retry_after"])
      
      if "message" not in response_json:
        raise UnknownError(f"couldn't parse the response -> {response_json}", -1)
      
      raise UnknownError(response_json["message"], response_json.get("code") or -1, response_json.get("errors"))

    return not response_json["taken"]
  
  def __print_prefix(self) -> str:
    return f"[{self.proxy.name}]: " if self.proxy is not None else "" 

  def __handle_username(self, name: str) -> bool:
    prefix = self.__print_prefix()

    try:
      valid = self.check_username_valid(name)

      if valid:
        print(f"{prefix}'{name}' is valid for discord")
      
      return valid
    except RateError as err:
      self.__handle_rate_limit(err)
      time.sleep(err.time + 1)
      return self.__handle_username(name)
    except Exception as err:
      self.__handle_error(err)
      return False  

  def __handle_error(self, err):
    prefix = self.__print_prefix()
    print(Fore.RED + f"{prefix}> {err}" + Fore.RESET)

  def __handle_rate_limit(self, err):
    prefix = self.__print_prefix()
    print(Fore.RED + f"{prefix}> Rate Limited for {err.time} secs, waiting" + Fore.RESET)

  def run(self):
    muts = [Repeat(), Prefix(amount=3), Sufix(), Digitize(amount=2)]
    while True:
      for name in self.generator.generate(min_length=2, max_length=10):
        if self.__handle_username(name.get_main()):
          continue

        for sub in name.get_subs(muts=muts):
          self.__handle_username(sub)