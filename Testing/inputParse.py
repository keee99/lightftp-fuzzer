import os
import re


def seed_input(SEED_DIR):
    
    dir = os.fsencode(SEED_DIR)
    
    out = []
    for file in os.listdir(dir):
     filename = os.fsdecode(file)
     if filename.endswith(".txt"): 
        try:
            f = open(SEED_DIR + "/" + filename, "rt")
            out.append(parse_file(f))
        except:
            print(filename, "failed to open/parse")
     else:
         continue

    return out

def parse_file(f):
    out = []
    file_tests = f.read().split("---")
    for test in file_tests:

        test_struct =  {
                            "_input": [],
                            "_expect": [],
                            "_assert": []
                        }

        data = test.split("\n")
        
        for datum in data:
            in_out =  re.search("IN '(.*)' OUT '(.*)'", datum)
            if in_out:
                test_struct["_input"].append(in_out.group(1))
                test_struct["_expect"].append(in_out.group(2))
                
                continue

            assertion =  re.search("ASSERT '(.*)'", datum)
            if assertion:
                test_struct["_assert"].append(assertion.group(1))
        
        out.append(test_struct)        
        

    return out