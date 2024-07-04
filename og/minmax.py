import string
import random

class MinMax:
  def __init__(self, min_length: int, max_length: int):
    self._min_length = min_length
    self._max_length = max_length

  def check_for_length(self, s: str) -> str | None:
    return check_for_length(s, self._min_length, self._max_length)
  
def check_for_length(s: str, min: int, max: int) -> str | None:
  if max >= len(s) >= min:
    return s
  
  return None