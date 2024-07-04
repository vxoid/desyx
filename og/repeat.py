import random
from .mut import Mut
from typing import List

class Repeat(Mut):
  def __init__(self, amount: int = 1):
    super().__init__()
    self.amount = amount

  def mutate(self, og: str, min_length: int, max_length: int) -> List[str]:
    return [random.choice(og) * random.randint(min_length, max_length) for _ in range(self.amount)]