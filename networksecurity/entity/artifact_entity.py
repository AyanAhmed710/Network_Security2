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