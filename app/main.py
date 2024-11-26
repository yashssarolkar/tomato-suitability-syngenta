from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# Set base directory relative to current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Load the models
score_model = joblib.load(os.path.join(MODELS_DIR, 'suitability_score_model.pkl'))
label_model = joblib.load(os.path.join(MODELS_DIR, 'suitability_label_model.pkl'))
yield_model = joblib.load(os.path.join(MODELS_DIR, 'expected_yield_model.pkl'))

# Initialize FastAPI app
app = FastAPI()

# Mount static files directory to serve CSS and other assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    # Return the HTML form page
    return HTMLResponse(content=open('app/templates/index.html').read(), status_code=200)

# Pydantic schemas for input data and prediction response
class InputData(BaseModel):
    region: str
    soil_type: str
    variety: str
    season: str
    # Add other input features as required for your model

class Prediction(BaseModel):
    suitability_score: float
    suitability_label: str
    expected_yield: float

# Prediction endpoint
@app.post("/predict", response_model=Prediction)
def predict(data: InputData):
    # Convert input data to a DataFrame
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])

    # One-hot encode categorical variables
    categorical_columns = ['region', 'soil_type', 'variety', 'season']
    input_df = pd.get_dummies(input_df, columns=categorical_columns)

    # Align input with model features
    all_features = pd.DataFrame(columns=score_model.booster_.feature_name())
    input_df = input_df.reindex(columns=all_features.columns, fill_value=0)

    # Make predictions
    suitability_score = score_model.predict(input_df)[0]
    suitability_label = label_model.predict(input_df)[0]
    expected_yield = yield_model.predict(input_df)[0]

    # Return predictions (ensure keys match the Prediction schema)
    return {
        "suitability_score": suitability_score,
        "suitability_label": suitability_label,
        "expected_yield": expected_yield
    }