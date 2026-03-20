import os
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
import yaml
import numpy as np

import sys
import pickle

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
    

def save_numpy_array(data: np.array, file_path: str):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, data)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def save_object(file_path :str , obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            pass
    except Exception as e:
        raise NetworkSecurityException(e, sys)