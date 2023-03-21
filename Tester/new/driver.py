
from env import PRINT_TEST_LOGS, SH_GCOV_RUN_PATH, SH_MAKE_PATH, SH_START_LFTP_PATH
from parsers.config_parser import Config
from parsers.test_parser import TestDesc, TestParser
import pexpect
import re
from subprocess import Popen, run, PIPE, STDOUT
import traceback
from typing import List

import time

class TestSummary:
    def __init__(self, result: bool, input: List[str]) -> None:
        self.result = result
        self.input = input

    def __str__(self) -> str:
        return f"Test: result={'PASS' if self.result else 'FAIL'}, input={self.input})"

    def __repr__(self) -> str:
        return self.__str__()
    


# This class is responsible for executing the tests with a given input
class FTPTestDriver:

    def __init__(self, tests: List[TestDesc], config: Config) -> None:
        self.ftp_cfg = config
        self.tests = tests

        print("running make clean, make")
        self._ftp_clean_make();


    # Main func for test execution
    def run(self, test_input):

        ftp_server = self._spawn_ftp_server()
        time.sleep(0.1) # Sleep to allow threaded server instance to spawn

        test_result = self.run_test(test_input)

        self._close_ftp_server(ftp_server)
        
        print(test_result)
        self._run_gcov()
        return test_result


    def run_sh(self, file_path: str) -> None:
        run(["chmod", "+x", file_path], stdout=PIPE, stderr=STDOUT)
        run(["/bin/sh", file_path], stdout=PIPE, stderr=STDOUT)
        
    def _ftp_clean_make(self):
        self.run_sh(SH_MAKE_PATH)

    def _run_gcov(self):
        self.run_sh(SH_GCOV_RUN_PATH)

    def _spawn_ftp_server(self):
        run(["chmod", "+x", SH_START_LFTP_PATH])
        # return Popen(["/bin/sh", SH_START_LFTP_PATH], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        return pexpect.spawn("./" + SH_START_LFTP_PATH)

    def _close_ftp_server(self, ftp_server: Popen) -> None:
        # ftp_server.terminate() # TODO: Does force termination work here? Check if coverage is updated on force termination
        ftp_server.sendline("q")


    # Connect to FTP server
    def _spawn_ftp_conn(self):
        return pexpect.spawn(f'ftp ftp://{self.ftp_cfg.uname}:{self.ftp_cfg.pwd}@{self.ftp_cfg.addr}:{self.ftp_cfg.port}')
    

    # Close FTP server connection
    def _close_ftp_conn(self, ftp):
        return ftp.sendline('quit')
    

    # Retrieve all available logs
    def _get_log(self, ftp):
        after = "" if not isinstance(ftp.after, bytes) \
                else ftp.after.decode("utf-8")
        
        before = "" if not isinstance(ftp.before, bytes) \
                else ftp.before.decode("utf-8")
        
        return before + after


    # Insert test input into test, replacing @0@, @1@, etc. with the corresponding indexed inputs
    def insert_input_into_test(self, test_input_arr: List[str], _input: List[str]):
        for idx, inpt in enumerate(test_input_arr):
            sub = re.search("@(.*)@", inpt)
            if sub and sub.group(1).isnumeric():
                # Replace input with test input
                print("Input:", inpt, _input[int(sub.group(1))])
                test_input_arr[idx] = _input[int(sub.group(1))]
                


    # Runs the test with the given input
    def run_test(self, input):
        if PRINT_TEST_LOGS: 
            print("\n======= NEW test =========")

        result = True
        
        ftp = self._spawn_ftp_conn()
        try:
            test_count = 0
            for test in self.tests:
                test_count += 1
                print("sub-test", test_count, end=" - ")

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
            self._close_ftp_conn(ftp)

        out = TestSummary(result, input)
        if PRINT_TEST_LOGS:
            print("======= END test ========= \n")

        return out
