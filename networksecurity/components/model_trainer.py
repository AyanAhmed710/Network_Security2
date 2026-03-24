import os
import sys 

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
from networksecurity.entity.artifact_entity import ModelTrainerArtifact ,DataTransformationArtifact
import mlflow



from networksecurity.utils import load_object ,save_object ,load_numpy_array ,write_yaml_file
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score ,evaluate_model

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomForestClassifier , GradientBoostingClassifier , AdaBoostClassifier)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score
import dagshub

model_trainer_logger =get_logger("ModelTrainer")



class ModelTrainer:
    def __init__(self , model_trainer_config : ModelTrainerConfig , data_transformation_artifact : DataTransformationArtifact ):
        try:
            model_trainer_logger.info("Model Trainer Initialised")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
           
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_matric(self , model , classification_metric):
        try:
            f1_score = classification_metric.f1_score
            precision = classification_metric.precision
            recall = classification_metric.recall

            with mlflow.start_run(run_name = "model_trainer") as mlflow_run:
                mlflow.log_params(model.get_params())
                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)
                mlflow.sklearn.log_model(model , "model")
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def train_model(self , x_train ,y_train ,x_test , y_test ):

        models={
            "LogisticRegression" : LogisticRegression()
            # "DecisionTreeClassifier" : DecisionTreeClassifier(),
            # "RandomForestClassifier" : RandomForestClassifier(),
            # "GradientBoostingClassifier" : GradientBoostingClassifier(),
            # "AdaBoostClassifier" : AdaBoostClassifier(),
            # "KNeighborsClassifier" : KNeighborsClassifier()
        }


        params = {

                    "LogisticRegression": {
                    "penalty": ["l1"],
                    "C": [0.01],
                    "solver": ["liblinear"]  # supports l1 + l2
                },

                # "DecisionTreeClassifier": {
                #     "criterion": ["gini", "entropy"],
                #     "max_depth": [None, 5, 10, 20],
                #     "min_samples_split": [2, 5, 10],
                #     "min_samples_leaf": [1, 2, 4]
                # },

                # "RandomForestClassifier": {
                #     "n_estimators": [50, 100, 200],
                #     "max_depth": [None, 10, 20],
                #     "min_samples_split": [2, 5],
                #     "min_samples_leaf": [1, 2],
                #     "bootstrap": [True, False]
                # },

                # "GradientBoostingClassifier": {
                #     "n_estimators": [50, 100, 200],
                #     "learning_rate": [0.01, 0.1, 0.2],
                #     "max_depth": [3, 5, 7]
                # },

                # "AdaBoostClassifier": {
                #     "n_estimators": [50, 100, 200],
                #     "learning_rate": [0.01, 0.1, 1]
                # },

                # "KNeighborsClassifier": {
                #     "n_neighbors": [3, 5, 7, 9],
                #     "weights": ["uniform", "distance"],
                #     "metric": ["euclidean", "manhattan"]
                # }
            }
        

        report =evaluate_model(x_train , y_train , x_test , y_test , models , params)

        os.makedirs(os.path.dirname(self.model_trainer_config.report_file_path), exist_ok=True)

        write_yaml_file(file_path=self.model_trainer_config.report_file_path , data=report)

        best_model_score = max(sorted(report.values()))

        best_model_name = list(report.keys())[list(report.values()).index(best_model_score)]

        best_model = models[best_model_name]

        y_train_pred = best_model.predict(x_train)

        y_test_pred = best_model.predict(x_test)

        train_model_score = get_classification_score(y_train , y_train_pred)

        test_model_score = get_classification_score(y_test , y_test_pred)

        self.track_matric(best_model ,train_model_score)

        self.track_matric(best_model ,test_model_score)

        preprocessor =load_object(file_path=self.data_transformation_artifact.preprocessor_object_file_path)

        network_model =NetworkModel(preprocessor=preprocessor , model=best_model)

        os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path), exist_ok=True)

        save_object(file_path=self.model_trainer_config.trained_model_file_path , obj=network_model)

        model_trainer_artifact =ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
        train_metric_artifact=train_model_score,
        test_metric_artifact=test_model_score)

        return model_trainer_artifact


        


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            
            model_trainer_logger.info("Model Trainer Initialised")
            train_file_path= self.data_transformation_artifact.transformed_train_file_path
            test_file_path= self.data_transformation_artifact.transformed_test_file_path
            train_data = load_numpy_array(train_file_path)
            test_data = load_numpy_array(test_file_path)
            model_trainer_logger.info("Model Trainer data loaded successfully")

            x_train , y_train = train_data[:,:-1] , train_data[:,-1]
            x_test , y_test = test_data[:,:-1] , test_data[:,-1]

            model_trainer_logger.info("Model Trainer data split successfully")

            model_trainer_artifact =self.train_model(x_train , y_train ,x_test , y_test)

            



        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

        return model_trainer_artifact

