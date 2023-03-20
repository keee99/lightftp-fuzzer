import os
from datetime import datetime
from driver import TestSummary
from typing import List


# This class is responsible for collecting and writing test output
class OutputManager:
    def __init__(self) -> None:
        self.test_results = []
        self.test_inputs = []
        self.test_cov = []


    # Adds the output of a driver test into 
    def add_test_output(self, test_summary: TestSummary, test_cov) -> None:
        self.test_inputs.append(test_summary.input)
        self.test_results.append(test_summary.result)
        self.test_cov.append(test_cov)

    

    # TODO: write input and outputs too
    def write_final_output(self) -> str:
        
        #create output folder, change path
        output_file_path  = os.getcwd()+'/output'
        if not os.path.exists(output_file_path ):
            os.makedirs(output_file_path)

        #output_file_path = './output'

        #use timestamp to name file
        now = datetime.now()
        now_str = now.strftime("%d-%m-%y_%H:%M:%S")
        filename = now_str+".txt"

        #record tests that occured
        total_tests = len(self.test_results)
        total_pass=0
        total_fail=0
        log_str =''
        for i in range(len(self.test_results)):
            if self.test_results[i]==True:
                total_pass+=1
                log_str=log_str+"test case:" + str(self.test_inputs[i]) + "\n"+"pass"+"\n"
            elif self.test_results[i]==False:
                total_fail+=1
                log_str=log_str+"test case: "+ str(self.test_inputs[i]) + "\n"+"error"+"\n"
        
        pass_string = "{} out of {} test cases passed.".format(total_pass, total_tests)
        fail_string = "{} out of {} test cases failed.".format(total_fail, total_tests)

        try:
            with open(os.path.join(output_file_path, filename),"w") as f:
                f.write("Test at:"+now_str+"\n")
                f.write(pass_string+"\n")
                f.write(fail_string+"\n")
                f.write("\n" + log_str  + "\n")
                f.close()
        except FileNotFoundError:
            next
            
        return "log file written at " + output_file_path 