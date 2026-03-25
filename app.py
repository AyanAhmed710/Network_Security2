import sys
import os
import pymongo
import io
import pickle
import traceback
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
from networksecurity.pipeline.training_pipeline import Training_Pipeline
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response
import pandas as pd

from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME
)

# ─── Startup Diagnostics ─────────────────────────────────────────────────────
print("=" * 60)
print("[STARTUP] app.py is loading...")
print(f"[STARTUP] Python version: {sys.version}")
print(f"[STARTUP] Working directory: {os.getcwd()}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"[STARTUP] BASE_DIR: {BASE_DIR}")

# Check templates folder
templates_dir = os.path.join(BASE_DIR, "templates")
if os.path.exists(templates_dir):
    print(f"[STARTUP] Templates folder found: {templates_dir}")
    print(f"[STARTUP] Templates inside: {os.listdir(templates_dir)}")
else:
    print(f"[STARTUP] ❌ Templates folder MISSING at: {templates_dir}")

# Check model file
model_path = os.path.join(BASE_DIR, "final_model", "model.pkl")
if os.path.exists(model_path):
    print(f"[STARTUP] Model file found: {model_path}")
else:
    print(f"[STARTUP] ❌ Model file MISSING at: {model_path}")

# ✅ Clean single-line templates setup
try:
    templates = Jinja2Templates(directory=templates_dir)
    print("[STARTUP] ✅ Jinja2Templates initialized successfully")
except Exception as e:
    print(f"[STARTUP] ❌ Jinja2Templates init failed: {e}")
    traceback.print_exc()

# MongoDB connection
try:
    client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"), tlsCAFile=ca)
    database = client[DATA_INGESTION_DATABASE_NAME]
    collection = database[DATA_INGESTION_COLLECTION_NAME]
    print("[STARTUP] ✅ MongoDB connected successfully")
except Exception as e:
    print(f"[STARTUP] ❌ MongoDB connection failed: {e}")

print("[STARTUP] Starting FastAPI app...")
print("=" * 60)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    pipeline = Training_Pipeline()
    print("[STARTUP] ✅ Training_Pipeline initialized")
except Exception as e:
    print(f"[STARTUP] ❌ Training_Pipeline init failed: {e}")
    traceback.print_exc()


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/", tags=["authentication"])
async def index(request: Request):
    print("[GET /] Request received")
    try:
        print("[GET /] Attempting to render index.html...")
        response = templates.TemplateResponse("index.html", {"request": request})
        print("[GET /] ✅ index.html rendered successfully")
        return response
    except Exception as e:
        print(f"[GET /] ❌ Failed to render index.html")
        print(traceback.format_exc())
        return Response(f"Error rendering index: {str(e)}", status_code=500)


@app.get('/train')
async def train():
    print("[GET /train] Training started...")
    try:
        pipeline.run_pipeline()
        print("[GET /train] ✅ Training completed successfully")
        return Response("Training successful !!")
    except Exception as e:
        print(f"[GET /train] ❌ Training failed")
        print(traceback.format_exc())
        return Response(f"Error during training: {str(e)}", status_code=500)


@app.post('/predict')
async def predict(request: Request, file: UploadFile = File(...)):
    print("[POST /predict] Request received")
    try:
        # Step 1: Read uploaded file
        print(f"[POST /predict] Reading uploaded file: {file.filename}")
        contents = await file.read()
        print(f"[POST /predict] File size: {len(contents)} bytes")

        # Step 2: Parse CSV
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        print(f"[POST /predict] ✅ CSV parsed — shape: {df.shape}")
        print(f"[POST /predict] Columns: {df.columns.tolist()}")

        # Step 3: Load model
        print(f"[POST /predict] Loading model from: {model_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print(f"[POST /predict] ✅ Model loaded — type: {type(model)}")
        print(f"[POST /predict] Preprocessor type: {type(model.preprocessor)}")
        print(f"[POST /predict] Inner model type: {type(model.model)}")

        # Step 4: Predict
        print("[POST /predict] Running prediction...")
        y_pred = model.predict(df)
        print(f"[POST /predict] ✅ Prediction done — sample: {y_pred[:5]}")

        # Step 5: Append predictions to df
        df["predicted_column"] = y_pred
        print(f"[POST /predict] DF with predictions shape: {df.shape}")

        # Step 6: Save output
        output_dir = os.path.join(BASE_DIR, "prediction_output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "output.csv")
        df.to_csv(output_path, index=False)
        print(f"[POST /predict] ✅ Output saved to: {output_path}")

        # Step 7: Render template
        print("[POST /predict] Generating HTML table...")
        table_html = df.to_html(classes='table table-striped')
        print(f"[POST /predict] HTML table length: {len(table_html)} chars")

        print("[POST /predict] Rendering table.html template...")
        response = templates.TemplateResponse(
            "table.html",
            {"request": request, "table": table_html}
        )
        print("[POST /predict] ✅ Template rendered successfully — returning response")
        return response

    except Exception as e:
        print(f"[POST /predict] ❌ Error occurred")
        print(traceback.format_exc())
        return Response(f"Error: {str(e)}", status_code=500)


if __name__ == "__main__":
    app_run("app:app", host="0.0.0.0", port=8000)