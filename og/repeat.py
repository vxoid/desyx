import random
import string
from .mut import DeattachedMut
from typing import List

available_character = string.ascii_lowercase

class Repeat(DeattachedMut):
  def __init__(self, amount: int = 1):
    super().__init__()
    self.amount = amount

  def mutate(self, _, min_length: int, max_length: int) -> List[str]:
    return [random.choice(available_character) * random.randint(min_length, max_length) for _ in range(self.amount)]