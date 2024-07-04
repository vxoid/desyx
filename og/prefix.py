import string
import random
from .mut import Mut
from typing import List

prefixes = [
  "anti",
  "not",
  "de",
  "dis",
  "mid",
  "mis",
  "non",
  "over",
  "pre",
  "re",
  "semi",
  "sub",
  "un"
]

def get_random_prefix() -> str:
  return random.choice(prefixes + [random.choice(string.ascii_lowercase + string.digits) for i in range(len(prefixes))])

class Prefix(Mut):
  def __init__(self, amount = 1):
    super().__init__()
    self.amount = amount

  def _mutate_unchecked(self, og: str) -> List[str]:
    if True in [og.startswith(prefix) for prefix in prefixes]:
      return []

    result = []

    for _ in range(self.amount):
      result.append(get_random_prefix() + og)

    return result
