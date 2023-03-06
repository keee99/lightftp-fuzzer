from collections import deque
from typing import List
import random

class InputManager:
    def __init__(self) -> None:
        self.input_queue = deque()

    def choose_next(self):
        if len(self.input_queue):
            next = self.input_queue.popleft()

        return ["testdir" + str(random.randint(0, 1000))]
    
    def add_input(self, newInput: List[str]) -> None:
        self.input_queue.append(newInput)
