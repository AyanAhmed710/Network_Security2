import os
import sys
import pandas as pd
import numpy as np

#Common Constants

TARGET_COLUMN = "Result"
PIPELINE_NAME :str = "NetworkSecurity"
ARTIFACT_DIR :str = "Artifacts"
FILE_NAME="phisingData.csv"

TRAIN_FILE_NAME :str = "train.csv"
TEST_FILE_NAME :str = "test.csv"

#Data Ingestion Constants


DATA_INGESTION_DATABASE_NAME : str="Network_Security"
DATA_INGESTION_COLLECTION_NAME :str="Data"
DATA_INGESTION_DIR_NAME :str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str ="feature_store"
DATA_INGESTION_INGESTED_DIR_NAME :str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2
DATA_INGESTION_RANDOM_STATE :int = 42