from subprocess import run, Popen,  PIPE, STDOUT
from env import SH_START_LFTP_PATH
from time import sleep

run(["chmod", "+x", SH_START_LFTP_PATH])
pop = Popen(["/bin/sh", SH_START_LFTP_PATH], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
print("OPEN")
while (True):
    try:
        sleep(30)
        raise Exception
    except:
        print("terminating")
        # pop.terminate()
        try:
            grep_stdout = pop.communicate(input=b'q')[0]
            print(grep_stdout)
            sleep(30)
            raise Exception
        except:
            print("force Termination")
            pop.terminate()
        break


