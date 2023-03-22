from collections import deque
from driver import TestSummary
from env import SEED_PATH, INPUT_GEN_PATH
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
        self.seed_file_index = []

        seeds = SeedParser.seed_input(SEED_PATH)
        self.input_queue.append(seeds)
        
        # Seed files
        seed_files = SeedParser.get_seed_files()
        for file in seed_files:
            self.save_file(seeds["index"], file["content"])
            self.seed_file_index.append(file["index"])


    # Choose next input from input queue # TODO: Choose next input based on coverage
    def choose_next(self):
        # If seed queue is empty, seed it
        if not len(self.input_queue):
            self.add_input(SeedParser.seed_input(SEED_PATH))
        return self.input_queue.popleft()

    # Generate new inputs based on the output of the last test
    def generate_inputs(self, test_summary: TestSummary, test_cov) -> None:

        # do something with output data... --> is interesting, add_input, else random chance to add_input.
        
        # If interesting, add input (fuzz)
        self.add_input(test_summary.input) 


    # Add a new set of input and file input (for seeding) TODO: add Energy
    def add_input(self, oldInput: List[str]) -> None:
        fuzzed = list(map(self.fuzzer.fuzz, oldInput))

        self.input_queue.append(fuzzed)
        for i in self.seed_file_index:
            self.add_file_input(oldInput[i], fuzzed[i])
    

    # Add a new file input (for seeding)
    def add_file_input(self, oldFileName: str, newFileName: str) -> None:

        content = SeedParser.read_file_content(os.path.join(INPUT_GEN_PATH, oldFileName))
        for i in range(100):
            content = self.fuzzer.fuzz(content)
        self.save_file(newFileName, content)
        
        # self.rm_file(INPUT_GEN_PATH, oldFileName)




    # TODO: Shift to some file manager ==============
    # Saves a file
    def save_file(self, file_name: str, file_content=None):
        # Create the file with the random filename
        try:
            
            if not os.path.exists(INPUT_GEN_PATH):
                os.makedirs(INPUT_GEN_PATH)

            with open(os.path.join(INPUT_GEN_PATH, file_name), 'w') as f:
                f.write(file_content)
                f.close()
                
        except FileNotFoundError: # Exception error where the file cannot be created
            print("file not found")
        except OSError: # Exception error where the file cannot be written into
            print("os error wyd")

    def rm_file(self, input_path: str, file_name: str):
        try:
            os.remove(os.path.join(input_path, file_name, '.txt'))

        except FileNotFoundError: # Exception error where the file cannot be created
            print("file not found")
        except OSError: # Exception error where the file cannot be written into
            print("os error wyd")

            



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
    