import os
import re



from typing import List, Dict

# Test Description
class TestDesc:
    def __init__(self) -> None:
        self.inputs = []
        self.expects = []
        self.asserts = []
    
    def add_action(self, input: str, expect: str):
        self.inputs.append(input)
        self.expects.append(expect)
    
    def add_assertion(self, assertion: str):
        self.asserts.append(assertion)


# This class is responsible for parsing the test files into TestDesc objects
class TestParser:

    @classmethod
    def seed_test(cls, file_path: str) -> List[TestDesc]:
        file = os.fsencode(file_path)


        filename = os.fsdecode(file)

        if filename.endswith(".txt"): 
            try:
                f = open(filename, "rt")
                return cls._parse_file(f)
            
            except OSError:
                print(filename, "failed to open/parse")
        else:
            raise ValueError("file not .txt")
            


    @classmethod
    def _parse_file(cls, f) -> List[TestDesc]:
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
                    test_desc.add_assertion(assertion.group(1))
                    continue

                # Neither assertion not in_out --> raise ValueError
                # raise ValueError("Invalid test descriptor")
            
            out.append(test_desc)         

        return out
