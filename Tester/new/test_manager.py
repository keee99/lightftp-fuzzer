from constants import *
from driver import FTPTestDriver
from output_manager import OutputManager
from input_manager import InputManager

from parsers.config_parser import ConfigParser
from parsers.seed_parser import SeedParser
from parsers.test_parser import TestParser


class TestManager:

    def __init__(self) -> None:
        self.output_manager = OutputManager()
        self.input_manager = InputManager()
        
        self.config = ConfigParser.get_config(CONFIG_PATH, FTP_ACCOUNT)
        self.driver = FTPTestDriver(self.test, self.config)

    
    def run(self) -> None:
        self.test = TestParser.seed_test(TEST_PATH)  
        self.input_manager.add_input(SeedParser.seed_input(SEED_PATH))
        
        try:
            # Run tests until Keyboard Interrupt
            while True:
                next_input = self.input_manager.choose_next()
                test_result, test_input, test_output = self.driver.run(next_input)
                self.output_manager.add_test_output(test_result, test_input, test_output)

                # pass output to input manager to choose_next subsequently(?)
            

        except KeyboardInterrupt:
            self.output_manager.write_final_output(None)
            print("Bye!")
            return
    
