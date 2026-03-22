import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig


class NetworkModel:
    def __init__(self , preprocessor , model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def predict(self , features):
        try:
            preprocessed_features = self.preprocessor.transform(features)
            return self.model.predict(preprocessed_features)
        except Exception as e:
            raise NetworkSecurityException(e, sys)