import pexpect
import traceback

from mutate_parse import seed_input

#Retrieve these constants from nick's SWClient.py
FTP_UNAME = 'webadmin'
FTP_PWD = 'password'
FTP_ADDR = '127.0.0.1'
FTP_PORT = 8080
SEED_DIR = "/home/varsh389/LightFTPTesting/Tester/mutate_seed"

PRINT_TEST_LOGS = True



# Test input
#   _input and _expect same length --> each input gives an expected output
#   _assert: final assertions to validate final state
test_input = seed_input(SEED_DIR)



# Main func
def main():
    test_result = map(run_tests, test_input)
    print("test results:", list(test_result), "\n")



# Connect to FTP server
def spawn_ftp_conn():
    return pexpect.spawn(f'ftp ftp://{FTP_UNAME}:{FTP_PWD}@{FTP_ADDR}:{FTP_PORT}')

# Close FTP server connection
def close_ftp_conn(ftp):
    return ftp.sendline('quit')

# Retrieve all available logs
def get_log(ftp):
    after = "" if not isinstance(ftp.after, bytes) \
            else ftp.after.decode("utf-8")
    
    before = "" if not isinstance(ftp.before, bytes) \
            else ftp.before.decode("utf-8")
    
    return before + after



def run_tests(tests):
    if PRINT_TEST_LOGS: 
        print("\n======= NEW test =========")

    result = True
    ftp = spawn_ftp_conn()
    print(tests)
    try:
        for test in tests:
            _input = test["_input"]
            _expect = test["_expect"]
            _assert = test["_assert"]

            assert len(_input) == len(_expect)

            # iterate through and send the inputs
            for i in range(len(_input)):
                
                ftp.sendline(_input[i])
                ftp.expect(_expect[i])

            # Validation of test (requires some oracle?)
            for assertion in _assert:
                
                assert not assertion in get_log(ftp)
            
            if PRINT_TEST_LOGS:
                print(get_log(ftp))

    except pexpect.exceptions.EOF as e:
        print("EOF Exception -- Some expected output not found.")
        print(get_log(ftp))
        print(e.get_trace())
        result = False

    except: # including AssertionError
        print("Some exception occurred.")
        print(get_log(ftp))
        print(traceback.format_exc())
        result = False

    finally:
        close_ftp_conn(ftp)

    if PRINT_TEST_LOGS:
        print("======= END test ========= \n")
    return result



if __name__ == '__main__':
    main()
    