from collections import deque
from driver import TestSummary
from env import SEED_PATH, INPUT_GEN_PATH, ENERGY_FACTOR
import os
from parsers.seed_parser import SeedParser
import random
from typing import List


# This class is responsible for managing the input queue and generating the next input
class InputManager:
    def __init__(self) -> None:
        self.input_queue = deque()
        self.fuzzer = MutationRandomFuzzer()
        self.seed_file_index = []

        self.seeds = [SeedParser.seed_input(SEED_PATH)]
        for seed in self.seeds:
            self.input_queue.append(seed)
        
        # Seed files
        seed_files = SeedParser.get_seed_files()
        for i, file in enumerate(seed_files):
            self.save_file(self.seeds[i][file["index"]], file["content"])
            self.seed_file_index.append(file["index"])

            
        # seeds = SeedParser.seed_input(SEED_PATH)
        # self.input_queue.append(seeds)
        
        # # Seed files
        # seed_files = SeedParser.get_seed_files()
        # for file in seed_files:
        #     self.save_file(seeds[file["index"]], file["content"])
        #     self.seed_file_index.append(file["index"])

        self.highest_seen_cov = 0


    # Generate new inputs based on the output of the last test
    def generate_inputs(self, test_summary: TestSummary, test_cov) -> None:

        # do something with output data... --> is interesting, add_input, else random chance to add_input.
        if self.is_interesting(test_cov):
            self.seeds.append(test_summary.input)

        energy = self.assign_energy(test_cov)    
        
        # If interesting, add input (fuzz)

        for e in range(energy):
            self.add_input(test_summary.input) 


    # Add a new set of input and file input (for seeding) TODO: add Energy
    def add_input(self, oldInput: List[str]) -> None:
        fuzzed = list(map(self.fuzzer.fuzz, oldInput))

        self.input_queue.append(fuzzed)

        # if there are files to fuzz and seed, create the files
        for i in self.seed_file_index:
            old_file_name = oldInput[i]
            new_file_name = fuzzed[i]

            content = SeedParser.read_file_content(os.path.join(INPUT_GEN_PATH, old_file_name))
            for i in range(100):
                content = self.fuzzer.fuzz(content)
            self.save_file(new_file_name, content)
    

    # GRAYBOX METHODS ===============================

    # Mark the test as interesting if test coverage improves from the previous test
    def is_interesting(self, test_cov) -> bool:
        if test_cov["statement_cov"]["cov"] > self.highest_seen_cov:
            self.highest_seen_cov = test_cov["statement_cov"]["cov"]
            return True
        return False
    
    # Choose the most interesting input from input queue as next input
    def choose_next(self) -> List[str]:
        # TODO: not done! --> record path frequency, choose lowest frequency path

        # If seed queue is empty, seed it with original seeds + interesting test cases found
        if not len(self.input_queue):
            for seed in self.seeds:
                self.add_input(seed)
        return self.input_queue.popleft()
        

    # Assign fuzzing energy to the input
    def assign_energy(self, test_cov) -> int:

        # Simple implementation that takes a multiple of coverage increase
        cov_increment = test_cov["statement_cov"]["cov"] - self.highest_seen_cov
        if cov_increment <= 0:
            cov_increment = 0

        
        return ENERGY_FACTOR * int(cov_increment)





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
            print("save file os error", file_name)

    def rm_file(self, input_path: str, file_name: str):
        try:
            os.remove(os.path.join(input_path, file_name, '.txt'))

        except FileNotFoundError: # Exception error where the file cannot be created
            print("file not found")
        except OSError: # Exception error where the file cannot be written into
            print("rm file os error", file_name, input_path)

            



class MutationRandomFuzzer:
    def fuzz(self, inpt):
        return self.flip(inpt)
    
    # Returns s with a random bit flipped in a random position
    def flip(self, s):
        if s == "":
            return s

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 1 << random.randint(0, 6)
        new_c = chr(ord(c) ^ bit)
        # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
        return s[:pos] + new_c + s[pos + 1:]
    
    