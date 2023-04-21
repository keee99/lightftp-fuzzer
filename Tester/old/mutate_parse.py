import os
import random
import re


def seed_input(SEED_DIR):
    
    dir = os.fsencode(SEED_DIR)
    
    out = []
    for file in os.listdir(dir):
     filename = os.fsdecode(file)
     if filename.endswith(".txt"): 
        # try:
            f = open("./mutate_seed/04.txt", "rt")
            out=parse_file(f)
        # except:
            # print(filename, "failed to open/parse")
     else:
         continue

    return out

def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]

def parse_file(f):
    out = []
    file_tests = f.read().split("---")
    inputval=None
    expectval=None
    assertval=None

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
                if(in_out.group(1)!=''):
                    inputval=in_out.group(1)
                    expectval=in_out.group(2)
                continue

            assertion =  re.search("ASSERT '(.*)'", datum)
            if assertion:
                    test_struct["_assert"].append(assertion.group(1))
                    assertval=assertion.group(1)
        
        
        out.append([test_struct])
        
        if(inputval and expectval and assertval):
            print('hello')
            for i in range(2):
                test_struct =  {
                            "_input": [],
                            "_expect": [],
                            "_assert": []
                        }
                inputmut=flip_random_character(inputval)
                print(inputmut)
                test_struct["_input"].append(inputmut)
                test_struct["_input"].append('')
                
                test_struct["_expect"].append(expectval)
                test_struct["_expect"].append('ftp> ')
                
                test_struct["_assert"].append(assertval)
                

                out.append([test_struct])        
        

    return out