from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint


@app.get("/")
def root():
    return {"message": "Server is running 🚀"}

# Data endpoint


@app.get("/data")
def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "data", "my_data.csv")
    df = pd.read_csv(file_path)

    # Convert NaN to None (JSON safe)
    df = df.astype(object).where(pd.notnull(df), None)

    return df.to_dict(orient="records")

# Upload endpoint


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    upload_path = os.path.join(
        os.path.dirname(__file__), "data", file.filename)

    with open(upload_path, "wb") as f:
        f.write(contents)

    return {"filename": file.filename, "message": "Upload successful"}

app = FastAPI()

# Allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data")
def get_data():
    return [
        {"name": "Item A", "value": 10},
        {"name": "Item B", "value": 20},
    ]
