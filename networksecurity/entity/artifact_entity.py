import os
from dataclasses import dataclass
from networksecurity.entity.config_entity import DataIngestionConfig


@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str

    def __str__(self) -> str:
        return f"DataIngestionArtifact(feature_store_file_path={self.feature_store_file_path}, train_file_path={self.train_file_path}, test_file_path={self.test_file_path})"
    

@dataclass
class DataValidationArtifact:
    validation_status : bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

    def __str__(self) -> str:
        return f"DataValidationArtifact(valid_train_file_path={self.valid_train_file_path}, valid_test_file_path={self.valid_test_file_path}, invalid_train_file_path={self.invalid_train_file_path}, invalid_test_file_path={self.invalid_test_file_path}, drift_report_file_path={self.drift_report_file_path})"
    

@dataclass
class DataTransformationArtifact :
    transformed_train_file_path : str
    transformed_test_file_path : str
    preprocessor_object_file_path : str