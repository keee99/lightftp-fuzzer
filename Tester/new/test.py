
from parsers.coverage_parser import CoverageParser
from env import COVERAGE_PATH

print(CoverageParser.get_cov(COVERAGE_PATH))