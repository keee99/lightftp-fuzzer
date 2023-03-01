import pexpect
import traceback

from inputParse import seed_input
from mutate_parse import seed_input
from configParser import retrieve_account_details,retrieve_config_details,set_config

# Check port in cfg file is not 21 and change to 80 if it is
configDetails = retrieve_config_details()
if configDetails['port']==21:
    set_config('ftpconfig',"port",8080)

# Retrieve local target folder and store in dict
accountDetails = retrieve_account_details()
# target_folder = accountDetails[account]['root']


#Retrieve these constants from nick's SWClient.py
FTP_UNAME = 'webadmin'
FTP_PWD = accountDetails[FTP_UNAME]['pswd'] #'password'
FTP_ADDR = configDetails['interface'] #'127.0.0.1'
FTP_PORT = configDetails['port'] #8080
SEED_DIR = "./seed"

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
                
                assert assertion in get_log(ftp)
            
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
    