import logging
import sys

def add_logging_config():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    #logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))