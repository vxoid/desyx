import random
from .mut import Mut
from typing import List

class Digitize(Mut):
  def __init__(self, amount = 1):
    super().__init__()
    self.amount = amount

  def _mutate_unchecked(self, og: str) -> List[str]:
    char_to_num = {
      'o': '0',
      'i': '1',
      'z': '2',
      'e': '3',
      'a': '4',
      's': '5',
      'g': '6',
      't': '7',
      'b': '8',
      'p': '9',
    }
    digitable = []

    for i, char in enumerate(og):
      if char in char_to_num:
        digitable.append(i)

    if len(digitable) == 0:
      return []

    result = []
    for _ in range(self.amount):
      change = random.choice(digitable)
      new_chars = []
      for i, c in enumerate(og):
        if i == change:
          new_chars.append(char_to_num[c])
        else:
          new_chars.append(c)

      result.append(''.join(new_chars))

    return result