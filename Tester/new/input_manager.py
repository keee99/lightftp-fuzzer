from collections import deque
from env import SEED_PATH
from parsers.seed_parser import SeedParser
from typing import List
import random

# This class is responsible for managing the input queue and generating the next input
class InputManager:
    def __init__(self) -> None:
        self.input_queue = deque()


    # Choose next input from input queue
    def choose_next(self):
        # If seed queue is empty, seed it
        if not len(self.input_queue):
            self.add_input(SeedParser.seed_input(SEED_PATH))
        return self.input_queue.popleft()
            


    # Add a new set of input (for seeding)
    def add_input(self, newInput: List[str]) -> None:
        self.input_queue.append(newInput)


    # Generate new inputs based on the output of the last test
    def generate_inputs(self, output_data) -> None:

        # do something with output data...

        self.add_input(["testdir" + str(random.randint(0, 1000))]) # Dummy input generation for now
                        
        # TODO: fuzzing is not yet done. Use Varsh's and NickHo's impl.
        #       Pass output (or cov info) into here

