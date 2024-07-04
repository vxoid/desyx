import string
import random
from .mut import Mut
from typing import List

sufixes = [
  "able",
  "ible",
  "al",
  "ed",
  "en",
  "er",
  "est",
  "ful",
  "ic",
  "ing",
  "ion",
  "tion",
  "ation",
  "ition",
  "ity",
  "ty",
  "ive",
  "ative",
  "itive",
  "less",
  "ly",
  "ment",
  "ness",
  "ous",
  "eous",
  "ious"
]

def get_random_sufix() -> str:
  return random.choice(sufixes + [random.choice(string.ascii_lowercase + string.digits) for i in range(len(sufixes))])

class Sufix(Mut):
  def __init__(self, amount = 1):
    super().__init__()
    self.amount = amount

  def _mutate_unchecked(self, og: str) -> List[str]:
    if True in [og.endswith(sufix) for sufix in sufixes]:
      return []

    result = []

    for _ in range(self.amount):
      result.append(og +  get_random_sufix())

    return result
