import sys
import os
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils import load_object

import certifi
ca =certifi.where()

from dotenv import load_dotenv
load_dotenv()

from networksecurity.pipeline.training_pipeline import Training_Pipeline
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run

from fastapi import FastAPI ,File ,UploadFile ,Request
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME

from fastapi.templating import Jinja2Templates


client =pymongo.MongoClient(os.getenv("MONGO_DB_URL"))
database =client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


mongo_db_url=os.getenv("MONGO_DB_URL")

pipeline=Training_Pipeline()

templates=Jinja2Templates(directory="./templates")





@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get('/train')
async def train():
    try:
        pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    

@app.post('/predict')
async def predict(request  : Request ,file: UploadFile = File(...)):

    try:
        df =pd.read_csv(file.file)
        # preprocessor =load_object("preprocessor.pkl")
        model = load_object(r"D:\MLOPS\Network_Security2\Network_Security2\final_model\model.pkl")
        # pipeline=NetworkModel(preprocessor , model)
        y_pred=model.predict(df)

        df["predicted_column"] = y_pred
        print(df["predicted_column"])

        df.to_csv(r"D:\MLOPS\Network_Security2\Network_Security2\prediction_output\output.csv")

        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
    except Exception as e:
        return Response(f"Error Occurred! {e}")

    

if __name__ == "__main__":
    app_run("app:app", host="localhost", port=8000)
