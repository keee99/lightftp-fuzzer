import os
from datetime import datetime
from typing import List, Dict

class OutputManager:
    def __init__(self) -> None:
        self.test_results = []
        self.test_inputs = []
        self.test_outputs = []


    # Adds the output of a driver test into 
    def add_test_output(self, result: bool, inputs: List, outputs: List, *other):
        self.test_inputs.append(input)
        self.test_outputs.append(outputs)
        self.test_results.append(result)
    

    # TODO: write input and outputs too
    def write_final_output(self, test_result):
        
        #create output folder, change path
        output_file_path  = os.getcwd()+'/output'
        if not os.path.exists(output_file_path):
            os.makedirs(output_file_path)

        #output_file_path = './output'

        #use timestamp to name file
        now = datetime.now()
        now_str = now.strftime("%d-%m-%y_%H:%M:%S")
        filename = now_str+".txt"

        #record tests that occured
        total_tests = len(test_result)
        total_pass = sum(test_result)
        pass_string = "{} out of {} test cases passed.".format(total_pass, total_tests)
        total_fail =  total_tests - total_pass
        fail_string = "{} out of {} test cases failed.".format(total_fail, total_tests)

        try:
            with open(os.path.join(output_file_path, filename),"w") as f:
                f.write("Test at:"+now_str+"\n")
                f.write(pass_string+"\n")
                f.write(fail_string+"\n")
                f.close()
        except FileNotFoundError:
            print(now_str + '\n' + pass_string + '\n' + fail_string)
            print("File not found, output not saved.")

        return test_result