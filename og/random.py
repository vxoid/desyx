import random
import string
from typing import List
from .mut import DeattachedMut

available_character = string.ascii_lowercase + string.digits

class Random(DeattachedMut):
  MAX_LENGTH = 3
  def __init__(self, amount = 1):
    super().__init__()
    self.amount = amount

  def mutate(self, _, min_length: int, max_length: int) -> List[str]:
    max_length = Random.MAX_LENGTH if max_length > Random.MAX_LENGTH else max_length
    if min_length > max_length:
      return []
    
    result = []

    for _ in range(self.amount):
      result.append("".join([random.choice(available_character) for _ in range(random.randint(min_length, max_length))]))

    return result