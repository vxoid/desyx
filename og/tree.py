from .mut import Mut
from .repeat import Repeat
from .prefix import Prefix
from .sufix import Sufix
from .digitize import Digitize
from .minmax import MinMax
from typing import List

class Tree(MinMax):
  def __init__(self, name: str, min_length: int, max_length: int):
    super().__init__(min_length, max_length)
    self.__name = name
  
  def get_main(self) -> str:
    return self.__name
  
  def get_semis(self, muts: List[Mut] = [Repeat(), Prefix(), Sufix(), Digitize()]) -> List[str]:
    return list(set([mut_name for mut in muts for mut_name in mut.mutate(self.__name, self._min_length, self._max_length)]))

  def __str__(self) -> str:
    return f"Tree({self._min_length} <= {self.__name} <= {self._max_length})"