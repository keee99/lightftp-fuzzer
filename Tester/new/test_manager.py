from env import *
from driver import FTPTestDriver
from output_manager import OutputManager
from input_manager import InputManager
from time import sleep
import traceback

from parsers.config_parser import ConfigParser
from parsers.coverage_parser import CoverageParser
from parsers.test_parser import TestParser


# This class is responsible for managing the entire testing pipeline
class TestManager:

    def __init__(self) -> None:
        # Create OutputManager and InputManager
        self.output_manager = OutputManager()
        self.input_manager = InputManager()
        
        # Create FTPTestDriver, which recompiles the ftp server 
        self.driver = FTPTestDriver(
                TestParser.seed_test(TEST_PATH), 
                ConfigParser.get_config(CONFIG_PATH, FTP_ACCOUNT)
            )


    
    # Execute the tests configured in driver and write the output to a file
    def run(self) -> None:
        try:
            # while True:
            for x in range(NUM_TESTS):

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
                
                sleep(0.2)

        except KeyboardInterrupt:
            "Keyboard interrupt - end tests"
        except:
            traceback.print_exc()

        finally:
            print(self.output_manager.write_final_output())
            print("Bye!")
            return
    
