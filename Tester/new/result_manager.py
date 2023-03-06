
class ResultManager:
    def __init__(self) -> None:
        self.output_manager = OutputManager()
        self.input_manager = InputManager()
        
        self.config = ConfigParser.get_config(CONFIG_PATH, FTP_ACCOUNT)
        self.test = TestParser.seed_test(TEST_PATH)  
        self.input_manager.add_input(None) # Unimpl: Parse initial seed

        self.driver = FTPTestDriver(self.test, self.config)

    
    def run(self) -> None:
        try:
            # Run tests until Keyboard Interrupt
            while True:
                next_input = self.input_manager.choose_next()
                test_result = self.driver.run(next_input)
                # Manage output, pass data into input_manager if needed
                pass

        except KeyboardInterrupt:
            OutputManager.write_final_output(None)
            print("Bye!")
            return