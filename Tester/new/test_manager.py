from env import *
from driver import FTPTestDriver
from output_manager import OutputManager
from input_manager import InputManager
from time import sleep

from parsers.config_parser import ConfigParser
from parsers.seed_parser import SeedParser
from parsers.test_parser import TestParser


# This class is responsible for managing the entire testing pipeline
class TestManager:

    def __init__(self) -> None:
        # Create OutputManager and InputManager
        self.output_manager = OutputManager()
        self.input_manager = InputManager()
        
        self.config = ConfigParser.get_config(CONFIG_PATH, FTP_ACCOUNT)
        self.driver = FTPTestDriver(TestParser.seed_test(TEST_PATH), self.config)
        self.input_manager.add_input(SeedParser.seed_input(SEED_PATH))

    
    def run(self) -> None:
        
        try:
            # Running tests until Keyboard Interrupt doesnt work if it interrupts a test.
            # while True:
            for x in range(NUM_TESTS):
                next_input = self.input_manager.choose_next()
                test_result, test_input = self.driver.run(next_input)
                self.output_manager.add_test_output(test_result, test_input)
                sleep(0.2)

                # pass output to input manager to choose_next subsequently(?)
                # TODO: fuzzing is not yet done. Use Varsh's and NickHo's impl
            

        except KeyboardInterrupt:
            "Keyboard interrupt - end tests"

        finally:
            print(self.output_manager.write_final_output())
            print("Bye!")
            return
    
