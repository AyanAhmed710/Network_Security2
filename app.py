# import sys
# import os
# import pymongo
# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import get_logger
# from networksecurity.utils.ml_utils.model.estimator import NetworkModel
# from networksecurity.utils import load_object

# import certifi
# ca =certifi.where()

# from dotenv import load_dotenv
# load_dotenv()

# from networksecurity.pipeline.training_pipeline import Training_Pipeline
# from fastapi.middleware.cors import CORSMiddleware
# from uvicorn import run as app_run

# from fastapi import FastAPI ,File ,UploadFile ,Request
# from fastapi.responses import Response
# from starlette.responses import RedirectResponse
# import pandas as pd

# from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

# from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME

# from fastapi.templating import Jinja2Templates


# client =pymongo.MongoClient(os.getenv("MONGO_DB_URL"))
# database =client[DATA_INGESTION_DATABASE_NAME]
# collection=database[DATA_INGESTION_COLLECTION_NAME]

# app=FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# mongo_db_url=os.getenv("MONGO_DB_URL")

# pipeline=Training_Pipeline()

# templates=Jinja2Templates(directory="./templates")





# @app.get("/", tags=["authentication"])
# async def index():
#     return RedirectResponse(url="/docs")


# @app.get('/train')
# async def train():
#     try:
#         pipeline.run_pipeline()
#         return Response("Training successful !!")
#     except Exception as e:
#         return Response(f"Error Occurred! {e}")
    

# @app.post('/predict')
# async def predict(request  : Request ,file: UploadFile = File(...)):

#     try:
#         df =pd.read_csv(file.file)
#         # preprocessor =load_object("preprocessor.pkl")
#         model = load_object(r"D:\MLOPS\Network_Security2\Network_Security2\final_model\model.pkl")
#         # pipeline=NetworkModel(preprocessor , model)
#         y_pred=model.predict(df)

#         df["predicted_column"] = y_pred
#         print(df["predicted_column"])

#         df.to_csv(r"D:\MLOPS\Network_Security2\Network_Security2\prediction_output\output.csv")

#         table_html = df.to_html(classes='table table-striped')

#         return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
#     except Exception as e:
#         return Response(f"Error Occurred! {e}")

    

# if __name__ == "__main__":
#     app_run("app:app", host="0.0.0.0", port=8000)


import sys
import os
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils import load_object
import io

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

from networksecurity.pipeline.training_pipeline import Training_Pipeline
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd


from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME

from fastapi.templating import Jinja2Templates

# Base directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"))
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_db_url = os.getenv("MONGO_DB_URL")

pipeline = Training_Pipeline()

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/train')
async def train():
    try:
        pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post('/predict')
async def predict(request: Request, file: UploadFile = File(...)): 
    try:

        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        

        # Relative path to model
        model_path = os.path.join(BASE_DIR, "final_model", "model.pkl")
        model = load_object(model_path)

        y_pred = model.predict(df)
        df["predicted_column"] = y_pred
        print(df["predicted_column"])

        # Create output directory if it doesn't exist
        output_dir = os.path.join(BASE_DIR, "prediction_output")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "output.csv")
        df.to_csv(output_path, index=False)

        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        return Response(f"Error Occurred! {e}")


if __name__ == "__main__":
    app_run("app:app", host="0.0.0.0", port=8000)
