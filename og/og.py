import random
from .tree import Tree
from typing import List

class Generator:
  def __init__(self, words_dict_file: str = "words.txt"):
    print("> this Generator piece of code was made by [VXIIIEATH], if you're redistributing this project you MUST either credit me as @VXIIIEATH or leave link on my social media like GITHUB.")

    with open(words_dict_file, 'r') as file:
      self.words = [word.lower() for word in file.read().split()]

    self.words = list(set([subword for word in self.words for subword in word.split('-')]))
    self.words = list(set([word.replace('\'', '').replace('\"', '') for word in self.words]))

  def generate(self, min_length: int = 5, max_length: int = 15, amount: int = 30) -> List[Tree]:
    return [Tree(word, min_length, max_length) for word in random.choices([word for word in self.words if max_length > len(word) >= min_length], k=amount)]