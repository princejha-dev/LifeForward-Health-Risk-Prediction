from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add src to python path to import predict module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from predict import load_model, predict_health

app = FastAPI(
    title="NovaGen Health Prediction API",
    description="API for predicting health risks using our Random Forest Model",
    version="1.0.0"
)

# Load the model on startup
try:
    model = load_model("models/health_model.pkl")
except Exception as e:
    model = None
    print(f"Warning: Model not loaded. {e}")

class HealthData(BaseModel):
    Age: float
    BMI: float
    Blood_Pressure: float
    Cholesterol: float
    Glucose_Level: float
    Heart_Rate: float
    Sleep_Hours: float
    Exercise_Hours: float
    Water_Intake: float
    Stress_Level: float
    Smoking: int
    Alcohol: int
    Diet: int
    MentalHealth: int
    PhysicalActivity: int
    MedicalHistory: int
    Allergies: int
    Diet_Type__Vegan: bool
    Diet_Type__Vegetarian: bool
    Blood_Group_AB: bool
    Blood_Group_B: bool
    Blood_Group_O: bool

@app.get("/")
def read_root():
    return {"message": "Welcome to the NovaGen Health Prediction API. Use POST /predict to get health risk predictions."}

@app.post("/predict")
def predict(data: HealthData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded. Please train the model first.")
        
    # Convert Pydantic model to dictionary
    input_dict = data.dict()
    
    try:
        # Get prediction
        prediction_result = predict_health(model, input_dict)
        return {"prediction": prediction_result[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
