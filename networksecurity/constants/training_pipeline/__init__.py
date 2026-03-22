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

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

#Data Ingestion Constants


DATA_INGESTION_DATABASE_NAME : str="Network_Security"
DATA_INGESTION_COLLECTION_NAME :str="Data"
DATA_INGESTION_DIR_NAME :str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str ="feature_store"
DATA_INGESTION_INGESTED_DIR_NAME :str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2
DATA_INGESTION_RANDOM_STATE :int = 42

#Data Validation Constants

DATA_VALIDATION_DIR_NAME :str="data_validation"
DATA_VALIDATION_VALID_DIR :str="validated"
DATA_VALIDATION_INVALID_DIR :str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR :str="drift_report"
DATA_VALIDATION_DRIFT_FILE_NAME :str="report.yaml"



#Data Transformation Constants

DATA_TRANSFORMATION_DIR_NAME :str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR :str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME :str="transformed_train.npy"
DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME :str="transformed_test.npy"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME :str="transformer.pkl"

#knn imputer to replae missing values
DATA_TRANSFORMATION_IMPUTER_PARAMS : dict ={
    "missing_values" :np.nan ,
    "n_neighbors" : 3,
    "weights" : "uniform",
}


#Model Trainer Constants

MODEL_TRAINER_DIR_NAME :str="model_trainer"
MODEL_TRAINING_REPORT_NAME :str="report.yaml"
MODEL_TRAINER_TRAINED_MODEL_DIR :str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME :str="model.pkl"
MODEL_TRAINER_EXPECTED_ACCURACY :float = 0.6
MODEL_UNDERFITTING_OVERFITTING_THRESHOLD :float = 0.05
