import os
import re



from typing import List, Dict

# Test Description
class TestDesc:
    def __init__(self) -> None:
        self.inputs = []
        self.expects = []
        self.asserts = []
    
    def add_action(self, input: str, expects: str):
        self.inputs.append(input)
        self.expects.append(expects)
    
    def add_assertion(self, assertion: str):
        self.asserts.append(assertion)

    

class TestParser:

    @classmethod
    def seed_test(cls, file_path: str) -> List[TestDesc]:
        file = os.fsencode(file_path)


        filename = os.fsdecode(file)

        if filename.endswith(".txt"): 
            try:
                f = open(file_path + "/" + filename, "rt")
                return cls._parse_file(f)
            
            except OSError:
                print(filename, "failed to open/parse")
        else:
            raise ValueError("file not .txt")
            


    @classmethod
    def _parse_file(cls, f) -> List(TestDesc):
        out = []
        file_tests = f.read().split("---")
        for test in file_tests:

            test_desc = TestDesc()

            data = test.split("\n")
            for datum in data:
                in_out =  re.search("IN '(.*)' OUT '(.*)'", datum)
                if in_out:
                    test_desc.add_action(input=in_out.group(1), expect=in_out.group(2))  
                    continue

                assertion =  re.search("ASSERT '(.*)'", datum)
                if assertion:
                    test_desc.add_assertion(assertion)
                    continue

                # Neither assertion not in_out --> raise ValueError
                raise ValueError("Invalid test descriptor")
            
            out.append(test_desc)         

        return out
