from typing import List
from abc import abstractmethod
from og.minmax import check_for_length

class Mut:
  def __init__(self):
    pass

  @abstractmethod
  def _mutate_unchecked(self, og: str) -> List[str]:
    raise NotImplementedError()
  
  def mutate(self, og: str, min_length: int, max_length: int) -> List[str]:
    result_unchecked = self._mutate_unchecked(og)
    return [name for name in result_unchecked if check_for_length(name, min_length, max_length) is not None]