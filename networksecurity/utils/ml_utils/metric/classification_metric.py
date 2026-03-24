import os
import sys
from networksecurity.logging.logger import get_logger
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score ,r2_score
from networksecurity.entity.artifact_entity import MetricsArtifiact
from sklearn.model_selection import GridSearchCV

def get_classification_score(y_true, y_pred):
    try:
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        return MetricsArtifiact(precision, f1, recall)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    


def evaluate_model(X_train ,Y_train ,X_test ,Y_test ,models ,params) -> dict:


    try:

        report={}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gt =GridSearchCV(model , param ,cv=5)
            gt.fit(X_train , Y_train)

            model.set_params(**gt.best_params_)

            model.fit(X_train, Y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(Y_train, y_train_pred)
            test_model_score = r2_score(Y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report


    except Exception as e:
        raise NetworkSecurityException(e, sys)


    