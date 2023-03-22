from collections import deque
from driver import TestSummary
from env import SEED_PATH
import os
from parsers.seed_parser import SeedParser
import random
import string
from typing import List


# This class is responsible for managing the input queue and generating the next input
class InputManager:
    def __init__(self) -> None:
        self.input_queue = deque()
        self.fuzzer = MutationRandomFuzzer()


    # Choose next input from input queue
    def choose_next(self):
        # If seed queue is empty, seed it
        if not len(self.input_queue):
            self.add_input(SeedParser.seed_input(SEED_PATH))
        return self.input_queue.popleft()
            

    # Add a new set of input (for seeding)
    def add_input(self, newInput: List[str]) -> None:

        # Energy = 100 hardcoded for now
        # for n in range(100):
        #     self.input_queue.append(list(map(self.fuzzer.fuzz, newInput)))

        self.input_queue.append(list(map(self.fuzzer.fuzz, newInput)))



    # Generate new inputs based on the output of the last test
    def generate_inputs(self, test_summary: TestSummary, test_cov) -> None:

        # do something with output data... --> is interesting?
        
        # If interesting, add input (fuzz)
        self.add_input(test_summary.input)

    

    def generate_rand_file(self, input_path: str, file_name: str, file_content=None):

        if file_content == None:
            letters = string.ascii_letters
            file_content = ''.join(random.choice(letters) for i in range(100))

        # Create the file with the random filename
        try:
            with open(os.path.join(input_path, file_name), 'w+') as f:
                f.write(self.fuzzer.fuzz(file_content))
                f.close()
        except FileNotFoundError: # Exception error where the file cannot be created
            pass
        except OSError: # Exception error where the file cannot be written into
            pass


    def rm_file(self, input_path: str, file_name: str):
        try:
            os.remove(os.path.join(input_path, file_name+ '.txt'))
        except FileNotFoundError: # Exception error where the file cannot be created
            pass
        except OSError: # Exception error where the file cannot be written into
            pass

            


class MutationRandomFuzzer:
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
    