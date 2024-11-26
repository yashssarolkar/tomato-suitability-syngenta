from pydantic import BaseModel

class InputData(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    temperature: float
    rainfall: float
    humidity: float
    sunlight: float
    pH: float
    N: float
    P: float
    K: float
    organic_carbon: float
    region: str
    soil_type: str
    variety: str
    season: str

class Prediction(BaseModel):
    suitability_score: float
    suitability_label: str
    expected_yield: float  # Original label retained
