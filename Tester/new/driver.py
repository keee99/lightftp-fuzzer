
from env import PRINT_TEST_LOGS
import logging
from parsers.config_parser import Config
from parsers.test_parser import TestDesc, TestParser
import pexpect
import re
import traceback
import subprocess,threading,time,os,signal
from typing import List



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


    # Main func for test execution
    def run(self, test_input):
        # Start Server
        server = pexpect.spawn("gnome-terminal --wait -- ./fftp", cwd="../../Source/Release" , encoding='utf-8')
        
        time.sleep(0.8)
        test_result = self.run_test(test_input)
        print(test_result)

        # Close Server
        server.close()
        server_pid = subprocess.check_output(["pidof","./fftp"])
        os.kill(int(server_pid.decode()),signal.SIGTERM)

        return test_result


    
    # TODO: spawn FTP server and close FTP server (to get cov data, and automate server starting process)
    # def start_server(self):
    #     pexpect.spawn("gnome-terminal -- ./fftp", cwd="../../Source/Release" , encoding='utf-8')

    # def stop_server(self):
    #     server_pid = subprocess.check_output(["pidof","./fftp"])
    #     print(server_pid.decode())
    #     os.kill(int(server_pid.decode()),signal.SIGTERM)

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
            self._close_ftp_conn(ftp)

        out = TestSummary(result, input)
        if PRINT_TEST_LOGS:
            print("======= END test ========= \n")
            
        return out
