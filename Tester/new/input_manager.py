from collections import deque
from driver import TestSummary
from env import SEED_PATH
from parsers.seed_parser import SeedParser
from typing import List
import random

# This class is responsible for managing the input queue and generating the next input
class InputManager:
    def __init__(self) -> None:
        self.input_queue = deque()
        self.fuzzer = BlackBoxFuzzer()


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
    def generate_inputs(self, test_summary: TestSummary) -> None:

        # do something with output data...
        
        # Apply fuzzing on all input
        self.add_input(list(map(self.fuzzer.fuzz, test_summary.input)))
                        
        # TODO: fuzzing is not yet done. Use Varsh's and NickHo's impl.
        #       Pass output (or cov info) into here
        #       Dont restrict to strings --> file/int --> implement a way to type the input



class BlackBoxFuzzer:
    def fuzz(self, inpt):
        return self.flip_random_character(inpt)
    
    def flip_random_character(self, s):
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return s

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 1 << random.randint(0, 6)
        new_c = chr(ord(c) ^ bit)
        # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
        return s[:pos] + new_c + s[pos + 1:]
    