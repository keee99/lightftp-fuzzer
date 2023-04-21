import os
import random
import re

from configParser import retrieve_account_details


accountDetails=retrieve_account_details()
FTP_DIR=accountDetails['webadmin']['root']

def seed_input(SEED_DIR):
    
    dir = os.fsencode(SEED_DIR)
    
    out = []
    for file in os.listdir(dir):
     filename = os.fsdecode(file)
     if filename.endswith(".txt"): 
        try:
            
            out.append(parse_file(SEED_DIR + "/" + filename, filename))
        except:
            print(filename, "failed to open/parse")
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
   
    return s[:pos] + new_c + s[pos + 1:]

def parse_file(f,fn):
    out = []

    inputval=None
    expectval=None
    assertval=None
        

    test_struct =  {
                        "_input": [],
                        "_expect": [],
                        "_assert": []
                    }

    
    test_struct["_input"].append('put')
    test_struct["_expect"].append('(local-file)')
    

    test_struct["_input"].append(f)
    test_struct["_expect"].append('(remote-file)')
    test_struct["_input"].append(FTP_DIR+'/'+fn)
    test_struct["_expect"].append('ftp> ')
    test_struct["_assert"].append('226')
   
    
    
    out.append(test_struct)
    

    return out