import os
from env import SEED_FILE
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
    
    # Takes a
    @classmethod
    def get_seed_files(cls):
        out = []
        if SEED_FILE != None:
            for file in SEED_FILE:
                path = file[0]
                filename_index = file[1]

                content = cls.read_file_content(path)
                name = os.path.basename(path)
                     

                out.append({"name": name, "content": content, "index": filename_index})
        
        return out
    
    @classmethod # TODO: shift to some file manager class
    def read_file_content(cls, file_path: str) -> str:
        try:
            content = ""
            with open(file_path,"r") as f:
                content += f.read()
                f.close()

            return content

        except FileNotFoundError:
            next
    

        
