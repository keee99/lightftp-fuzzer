

# General to change
# USER = "jj"
PRINT_TEST_LOGS = False
CLEAN_FILES = True
RUN_MODE = "TIME" # "TIME" or "NUM"

NUM_TESTS = 10
MIN_TO_RUN = 3

# Paths
CONFIG_PATH = '../../Source/Release/fftp.conf'
COVERAGE_PATH = "../../Source/Release/ftpserv.gcov.json"
TEST_PATH = "./tests/put.txt"
SEED_PATH = "./seeds/put.txt"
INPUT_GEN_PATH = "./input"

SEED_FILE = [ 
    # [Path, filename input input_index]
    ["./seeds/putinput.txt", 2]
] 

# LightFTP
FTP_ACCOUNT = 'webadmin' 

# Graybox
ENERGY_FACTOR = 1
MAX_ENERGY = 5

# Shell scripts
SH_MAKE_PATH = "shCleanMake.sh"
SH_CONNECT_LFTP_PATH = "shConnectLightFTP.sh"
SH_GCOV_RUN_PATH = "shGcovRun.sh"
SH_START_LFTP_PATH = "shStartLightFTP.sh"
SH_CLEAN_PATH = "shClean.sh"
