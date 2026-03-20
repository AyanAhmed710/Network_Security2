import os
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
import yaml
# import dill
import sys

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
def write_yaml_file(file_path: str, data: dict):
    try:
        with open(file_path, 'w') as yaml_file:
            yaml.safe_dump(data, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)