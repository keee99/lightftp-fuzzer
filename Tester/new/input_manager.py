from driver import TestSummary
from env import SEED_PATH, INPUT_GEN_PATH, ENERGY_FACTOR, MAX_ENERGY, CLEAN_FILES, PRINT_TEST_LOGS
from math import ceil
import os
from parsers.seed_parser import SeedParser
import random
import string
import time
from typing import List


# This class is responsible for managing the input queue and generating the next input
class InputManager:
    def __init__(self) -> None:

        # self.input_queue = deque()

        # input queue map implementation for path record and selection
        # Key = path, Value = input
        # Seed: key = "", value = seed input (path unknown)
        self.input_queue = {}


        self.fuzzer = MutationRandomFuzzer()
        self.seed_file_index = []

        self.seeds = [SeedParser.seed_input(SEED_PATH)]
        self.input_queue[""] = self.seeds
        
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
        self.path_freq_map = {} # Number of times a path has chosen
        self.path_gen_map = {} # Number of times a path has been generated


    # Generate new inputs based on the output of the last test
    def generate_inputs(self, test_summary: TestSummary, test_cov) -> None:
        
        if test_summary.result == "FAIL":
            return

        path, path_freq = self.get_and_set_path_freq(test_cov)

        # If is interesting, add input to seeds
        if self.is_interesting(test_cov):
            self.seeds.append(test_summary.input)

        # Assign energy to the input and fuzz based on energy
        energy = self.assign_energy(path_freq)    
        self.add_input(test_summary.input, exec_path=path, energy=energy) 

        if path in self.path_gen_map:
            self.path_gen_map[path] += energy
        else:
            self.path_gen_map[path] = 1           


    # Add and fuzz a new set of input and file input (for seeding)
    def add_input(self, oldInput: List[str], exec_path="", energy=1) -> None:

        file_name_charset = string.ascii_letters + string.digits + "()_-,."

        for e in range(energy):

            fuzzed = list(map(self.fuzzer.fuzz, oldInput, file_name_charset))

            # if there are files to fuzz and seed, create the files
            for i in self.seed_file_index:
                old_file_name = oldInput[i]
                new_file_name = fuzzed[i].replace(" ","_")

                # truncate file name if too long
                if len(new_file_name) > 255:
                    new_file_name = new_file_name[:255]
                    
                # if file name already exists in path, repeat the fuzz
                while os.path.exists(os.path.join(INPUT_GEN_PATH, new_file_name)):
                    new_file_name = self.fuzzer.fuzz(new_file_name, file_name_charset)
                    if len(new_file_name) > 255:
                        new_file_name = new_file_name[:255]

                fuzzed[i] = new_file_name

                content = SeedParser.read_file_content(os.path.join(INPUT_GEN_PATH, old_file_name))
                for j in range(100):
                    content = self.fuzzer.fuzz(content)
                self.save_file(new_file_name, content)
                
                
                print("Created file: " + new_file_name, " Input:", str(fuzzed[i]))


                print("Created file: " + new_file_name, " Input:", str(fuzzed[i]))


             # Add the input to the input queue corresponding to the previous exec path
            if exec_path in self.input_queue:
                self.input_queue[exec_path].append(fuzzed)
            else:
                self.input_queue[exec_path] = [fuzzed]
        
        # clean old files
        if CLEAN_FILES:
            for i in self.seed_file_index:
                old_file_name = oldInput[i]
                self.rm_file(INPUT_GEN_PATH, old_file_name)

        
    
        
    

    # GRAYBOX METHODS ===============================

    # Mark the test as interesting if test coverage improves from the previous test
    def is_interesting(self, test_cov) -> bool:
        if test_cov["statement_cov"]["cov"] > self.highest_seen_cov:
            self.highest_seen_cov = test_cov["statement_cov"]["cov"]
            return True
        return False
    
    # Choose the most interesting input from input queue as next input
    def choose_next(self) -> List[str]:

        # If seed queue is empty, seed it with fuzzed original seeds + interesting test cases found
        if not len(self.input_queue):
            for seed in self.seeds:
                self.add_input(seed)
        
        # Input queue is not empty, choose the next input
        # If queue contains seed, prioritize seed
        if "" in self.input_queue:
            path = ""
        else:
            path = self.get_lowest_freq_input_path()

        out = self.input_queue[path].pop(0)

        if path in self.input_queue and not len(self.input_queue[path]):
            self.input_queue.pop(path)
            
        return out
        

    # Assign fuzzing energy to the input
    def assign_energy(self, path_freq: int) -> int:

        result = 0
        mean_freq = self.get_mean_path_freq()

        if path_freq > mean_freq:
            result = 0
        else:
            result = min([
                MAX_ENERGY, 
                # Simple exponential function for energy
                ENERGY_FACTOR * ceil(pow(2, path_freq))])
        
        if PRINT_TEST_LOGS:
            print("Energy", result)

        return result



    # PATH FREQUENCY CALCULATIONS ============================

    def get_path(self, test_cov) -> str:
        test_cov_path = ""
        for line in test_cov["statement_cov"]["executed_lines"]:
            line_num = line["line_number"]
            test_cov_path += str(line_num) + ","
        return test_cov_path

    def get_and_set_path_freq(self, test_cov) -> None:
        path = self.get_path(test_cov)
        if path in self.path_freq_map:
            print("Path seen before, freq:", self.path_freq_map[path])
            self.path_freq_map[path] += 1
        else:
            print("Path newly explored")
            self.path_freq_map[path] = 1
        return path, self.path_freq_map[path]

    def get_mean_path_freq(self) -> int:
        return sum(self.path_freq_map.values()) / len(self.path_freq_map)
    
    def get_lowest_freq_input_path(self) -> str:
        input_path_freq_map = {k:v for (k,v) in self.path_freq_map.items() if k in self.input_queue}
        return min(input_path_freq_map, key=input_path_freq_map.get)


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
            print("file cannot be created:", file_name)
        except OSError: # Exception error where the file cannot be written into
            print("save file os error", file_name)

    def rm_file(self, input_path: str, file_name: str):
        try:
            os.remove(os.path.join(input_path, file_name))

        except FileNotFoundError: # Exception error where the file cannot be created
            print("rm file not found")
        except OSError: # Exception error where the file cannot be written into
            print("rm file os error", file_name, input_path)

            



class MutationRandomFuzzer:

    default_character_set = string.printable
    
    def fuzz(self, inpt, character_set=string.printable):
        if inpt == None:
            inpt = self.random_ascii_string(character_set)

        # Currently randomly chooses
        func = random.choice([
            # self.flip, 
            self.add, 
            self.delete, 
            # self.random_edge_case
        ])
        
        return func(inpt, character_set)
    
    # Returns s with a random bit flipped in a random position
    def flip(self, s, char_set):
        if s == "":
            return s

        new_c = ""
        while (True):
            pos = random.randint(0, len(s) - 1)
            c = s[pos]
            bit = 1 << random.randint(0, 6)
            new_c = chr(ord(c) ^ bit)
            if new_c in char_set:
                break

        # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
        return s[:pos] + new_c + s[pos + 1:]
    
    # Add a random ASCII character to the string at a random position
    def add(self, s, char_set):

        c = random.sample(char_set, 1)[0] #only printable ASCII characters
        # print("Adding", repr(c), "at position", pos)
        return self.insert(s, c)
    
    def insert(self, s, c):
        pos = random.randint(0, len(s))
        # print("Inserting", repr(c), "at position", pos)
        return s[:pos] + c + s[pos:]
    
    def delete(self, s, char_set):
        if s == "":
            return s

        pos = random.randint(0, len(s) - 1)
        # print("Deleting character at position", pos)
        return s[:pos] + s[pos + 1:]
    
    def random_ascii_string(self, char_set):
        return "".join([random.sample(char_set, 1)[0] for _ in range(10)]) #changed from 33,126 to 32,1126
    
    # Need change operator selection, or adapt test oracle to handle this
    def random_edge_case(self, s, char_set):

        edge_cases = [   
            "",             # Empty string
            random.sample(char_set, 1)[0] * 1000000,  # Very long string
            "2147483647",   # Max int
            "-2147483648",  # Min int
            random.sample(char_set, 1)[0], # Random Single character changed from 33,126 to 32,1126
            self.insert(s, random.choice(["\n", "\t", "\r", "\\"])), # Escape characters
        ]

        return random.choice(edge_cases)