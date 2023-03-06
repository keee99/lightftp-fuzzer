
from constants import PRINT_TEST_LOGS
import logging
from parsers.config_parser import Config
from parsers.test_parser import TestDesc, TestParser
import pexpect
import re
import traceback
from typing import List


# Currently the test_input is the TEST not the input, change that

class FTPTestDriver:

    def __init__(self, test: List[TestDesc], config: Config) -> None:
        self.ftp_cfg = config
        self.test = test


    # Main func
    def run(self, test_input):
        test_result = self.run_test(test_input)
        logging.info("test results:", list(test_result), "\n")



    # TODO: spawn FTP server and close FTP server (to get cov data)


    # Connect to FTP server
    def _spawn_ftp_conn(self):
        return pexpect.spawn(f'ftp ftp://{self.ftp_cfg.uname}:{self.ftp_cfg.pwd}@{self.ftp_cfg.addr}:{self.ftp_cfg.port}')
    

    # Close FTP server connection
    def _close_ftp_conn(ftp):
        return ftp.sendline('quit')
    

    # Retrieve all available logs
    def _get_log(ftp):
        after = "" if not isinstance(ftp.after, bytes) \
                else ftp.after.decode("utf-8")
        
        before = "" if not isinstance(ftp.before, bytes) \
                else ftp.before.decode("utf-8")
        
        return before + after


    def insert_input_into_test(self, test_input_arr: List(str), _input: List(str)):
        for idx, inpt in enumerate(test_input_arr):
            sub = re.search("@(.*)@", inpt)
            if sub and sub.group(1).isnumeric():
                # Replace input with test input
                print("Replacing input with test input:", inpt, _input[int(sub.group(1))])
                test_input_arr[idx] = _input[int(sub.group(1))]
                

    def run_test(self, input):
        if PRINT_TEST_LOGS: 
            print("\n======= NEW test =========")

        result = True
        
        ftp = self._spawn_ftp_conn()
        try:
            for test in self.tests:
                _input = test.inputs[:]
                _expect = test.expects
                _assert = test.asserts

                # Insert test input into test
                self.insert_input_into_test(_input, input)

                # iterate through and send the inputs
                for i in range(len(_input)):
                    
                    ftp.sendline(_input[i])
                    ftp.expect(_expect[i])

                # Validation of test (requires some oracle?)
                for assertion in _assert:
                    
                    assert assertion in self._get_log(ftp)
                
                if PRINT_TEST_LOGS:
                    print(self._get_log(ftp))

        except pexpect.exceptions.EOF as e:
            print("EOF Exception -- Some expected output not found.")
            print(self._get_log(ftp))
            print(e.get_trace())
            result = False

        except: # including AssertionError
            print("Some exception occurred.")
            print(self._get_log(ftp))
            print(traceback.format_exc())
            result = False

        finally:
            self.close_ftp_conn(ftp)

        if PRINT_TEST_LOGS:
            print("======= END test ========= \n")
        return result
