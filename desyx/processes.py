from multiprocessing import Process
from typing import List
import sys

class Processes:
  def __init__(self, processes: List[Process] = []):
    self.processes = processes
  
  def exit(self, signum, frame):
    print("Bye 👋")
    for p in self.processes:
      p.kill()
    sys.exit(0)