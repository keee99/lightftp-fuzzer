from collections import deque
from env import SEED_PATH
from parsers.seed_parser import SeedParser
from typing import List
import random

# This class is responsible for managing the input queue and generating the next input
class InputManager:
    def __init__(self) -> None:
        self.input_queue = deque()

    def choose_next(self):
        if len(self.input_queue):
            next = self.input_queue.popleft()

        return ["testdir" + str(random.randint(0, 1000))]
    
    def add_input(self, newInput: List[str]) -> None:
        self.input_queue.append(newInput)
