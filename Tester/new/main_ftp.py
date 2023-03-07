import logging
from test_manager import TestManager

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    TestManager().run()

if __name__ == '__main__':
    main()

