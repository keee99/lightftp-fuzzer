from env import *
from datetime import datetime, timedelta
from driver import FTPTestDriver
from output_manager import OutputManager
from input_manager import InputManager
from subprocess import run, PIPE, STDOUT
import traceback

from parsers.config_parser import ConfigParser
from parsers.coverage_parser import CoverageParser
from parsers.test_parser import TestParser


# This class is responsible for managing the entire testing pipeline
class TestManager:

    def __init__(self) -> None:
        
        # CLean the project
        run(["chmod", "+x", SH_CLEAN_PATH], stdout=PIPE, stderr=STDOUT)
        run(["/bin/sh", SH_CLEAN_PATH], stdout=PIPE, stderr=STDOUT)

        # Create OutputManager and InputManager
        self.output_manager = OutputManager()
        self.input_manager = InputManager()
        
        # Create FTPTestDriver, which recompiles the ftp server 
        self.driver = FTPTestDriver(
                TestParser.seed_test(TEST_PATH), 
                ConfigParser.get_config(CONFIG_PATH, FTP_ACCOUNT)
            )

    def run(self) -> None:
        try:
            if RUN_MODE == "NUM":
                for x in range(NUM_TESTS):
                    self._discrete_test()
            
            elif RUN_MODE == "TIME":
                end = datetime.now() + timedelta(minutes=MIN_TO_RUN)
                while datetime.now() < end:
                    self._discrete_test()    

        except KeyboardInterrupt:
            "Keyboard interrupt - end tests"
        except:
            traceback.print_exc()

        finally:
            print(self.output_manager.write_final_output())
            print("Bye!")
            return

        
    
    def _discrete_test(self) -> None:
        print("start new test")
        # Choose next input from input queue
        next_input = self.input_manager.choose_next()

        # Run the test and log the output
        test_summary = self.driver.run(next_input)
        test_cov = CoverageParser.get_cov(COVERAGE_PATH)

        self.output_manager.add_test_output(test_summary, test_cov)

        # Generate new inputs based on the output of the last test
        self.input_manager.generate_inputs(test_summary, test_cov)

        print("\n")
