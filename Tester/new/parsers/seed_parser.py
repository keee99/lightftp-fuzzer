import os
import traceback
from typing import List

# This class is responsible for parsing the seed file(s)
class SeedParser:
    
    @classmethod
    def seed_input(cls, file_path: str) -> List[str]:
        # TODO: multiple seeds
        file = os.fsencode(file_path)

        filename = os.fsdecode(file)

        if filename.endswith(".txt"): 
            try:
                f = open(filename, "rt")
                return cls._parse_file(f)
            
            except OSError:
                traceback.print_exc()
                print(filename, "failed to open/parse")
        else:
            raise ValueError("file not .txt")
        
    @classmethod
    def _parse_file(cls, f):
        inputs = f.read().strip().split()
        print("seeds:", inputs)
        return inputs