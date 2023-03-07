from env import *
from driver import FTPTestDriver, TestSummary
from output_manager import OutputManager
from input_manager import InputManager
from time import sleep

from parsers.config_parser import ConfigParser
from parsers.test_parser import TestParser


# This class is responsible for managing the entire testing pipeline
class TestManager:

    def __init__(self) -> None:
        # Create OutputManager and InputManager
        self.output_manager = OutputManager()
        self.input_manager = InputManager()
        
        # Create FTPTestDriver
        self.driver = FTPTestDriver(
            TestParser.seed_test(TEST_PATH), 
            ConfigParser.get_config(CONFIG_PATH, FTP_ACCOUNT)
            )


    
    # Execute the tests configured in driver and write the output to a file
    def run(self) -> None:
        try:
            # while True:
            for x in range(NUM_TESTS):

                next_input = self.input_manager.choose_next()

                # Run the test and log the output
                test_summary = self.driver.run(next_input)
                self.output_manager.add_test_output(test_summary)

                self.input_manager.generate_inputs(test_summary)
                
                sleep(0.2)

        except KeyboardInterrupt:
            "Keyboard interrupt - end tests"

        finally:
            print(self.output_manager.write_final_output())
            print("Bye!")
            return
    
