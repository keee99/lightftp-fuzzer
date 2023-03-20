
import json
from typing import List

class CoverageParser:

    @classmethod
    def get_cov(cls, file_path: str):

        statement_cov = cls.get_statement_cov(file_path)
        block_cov = cls.get_block_cov(file_path)
        # branch_cov = cls.get_branch_cov(file_path)
        
        return {
            "statement_cov": statement_cov,
            "block_cov": block_cov,
            # "branch_cov": branch_cov,
        }

    @classmethod
    def get_statement_cov(cls, file_path: str) -> float:
        cov_data = cls.parse_json(file_path)

        # ftpserv.c is index 0 of cov data.
        lines = cov_data["files"][0]["lines"] 

        # calculate total statement coverage
        executed_lines = [
                {
                    'line_number': line['line_number'],
                    'count': line['count']
                } for line in lines if line["count"] > 0]
        
        statement_cov = len(executed_lines) / len(lines) * 100
        
        # return statement_cov
        return {
            "cov": statement_cov,
            "executed_lines": executed_lines
        }
    

    @classmethod
    def get_block_cov(cls, file_path: str) -> float:
        cov_data = cls.parse_json(file_path)
        total_blocks = sum([f['blocks'] for f in cov_data["files"][0]["functions"]])
        executed_blocks = sum([f['blocks_executed'] for f in cov_data["files"][0]["functions"]])

        block_cov = executed_blocks / total_blocks * 100
        return {"cov": block_cov}


    # Branch coverage is not supported by gcovr
    # Branches attribute exists in lines, but it is always empty
    @classmethod
    def get_branch_cov(cls, file_path: str) -> List[str]:
        cov_data = cls.parse_json(file_path)
        branch_cov = 0
        return branch_cov
    
    
    # =========================
    # GCOV JSON format ========
    # =========================
    # gcc_version
    # files
    #   - file: "../ftpserv.c"
    #   - lines: {
    #               'branches': [], 
    #               'count': 100, 
    #               'line_number': 1778, 
    #               'unexecuted_block': False, 
    #               'function_name': 'ftpmain'
    #             }

    #   - functions: {
    #               'blocks': 32, 
    #               'end_column': 1, 
    #               'start_line': 1706, 
    #               'name': 'ftpmain', 
    #               'blocks_executed': 20, 
    #               'execution_count': 1, 
    #               'demangled_name': 'ftpmain', 
    #               'start_column': 7, 
    #               'end_line': 1784
    #               }
    # format_version
    # current_working_directory
    # data_file
    @classmethod
    def parse_json(cls, file_path: str) -> List[str]:
        try: 
            f = open(file_path, "r")
        except FileNotFoundError:
            print("Coverage file not found")
            exit()

        cov_data = json.load(f)


        # Closing file
        f.close()
        return cov_data
        
