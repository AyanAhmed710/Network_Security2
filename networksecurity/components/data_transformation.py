import os
import pandas as pd
import numpy as np
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from networksecurity.utils import save_numpy_array , save_object
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact ,DataValidationArtifact
from networksecurity.constants.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS


data_transformation_logger = get_logger("DataTransformation")


class DataTransformation:
    def __init__(self , data_transformation_config : DataTransformationConfig , data_validation_artifact : DataValidationArtifact):
        try:
            self.data_transformation_config : DataTransformationConfig = data_transformation_config
            self.data_validation_artifact : DataValidationArtifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    @staticmethod
    def read_data(file_path : str) -> pd.DataFrame:
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def get_transformer_object(self):
        data_transformation_logger.info("Getting transformer object.")

        try:
            knn=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            data_transformation_logger.info("Transformer object created.")

            processor :Pipeline = Pipeline(steps=[
                ("knn", knn),
            ])

            return processor


        except Exception as e:
            raise NetworkSecurityException(e, sys)
        


    def initiate_data_transformation(self):
        try:
            data_transformation_logger.info("Starting data transformation process.")

            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            train_features_out =train_df.drop(TARGET_COLUMN, axis=1)
            train_feature_target = train_df[TARGET_COLUMN]

            test_features_out = test_df.drop(TARGET_COLUMN, axis=1)
            test_feature_target = test_df[TARGET_COLUMN]

            train_feature_target = train_feature_target.replace(-1,0)
            test_feature_target = test_feature_target.replace(-1,0)

            processor = self.get_transformer_object()

            transformed_train_features = processor.fit_transform(train_features_out)
            transformed_test_features = processor.transform(test_features_out)

            train_arr =np.c_[transformed_train_features, np.array(train_feature_target)] 
            test_arr = np.c_[transformed_test_features, np.array(test_feature_target)]

            save_numpy_array(train_arr, self.data_transformation_config.transformed_train_file_path)
            save_numpy_array(test_arr, self.data_transformation_config.transformed_test_file_path)

            save_object(obj=processor, file_path=self.data_transformation_config.transformed_object_file_path)

            data_transformation_logger.info("Data transformation process completed.")


        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

        return DataTransformationArtifact(
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            preprocessor_object_file_path=self.data_transformation_config.transformed_object_file_path)

            

                      