import os
import joblib
import pandas as pd

def load_model(model_path="models/health_model.pkl"):
    """Loads the trained Random Forest model.""" # Make sure the train script ran first
    if not os.path.exists(model_path):
        # Fallback if run from the src folder
        model_path = "../models/health_model.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Please run train.py first.")
    
    return joblib.load(model_path)

def predict_health(model, input_data):
    """
    Makes a prediction on new data.
    `input_data` can be a single dictionary or a DataFrame matching the 22 features used in training.
    """
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])
        
    predictions = model.predict(input_data)
    
    # Target 1: Unhealthy/High Risk, 0: Healthy/Low Risk
    results = []
    for pred in predictions:
        if pred == 1:
            results.append("High Risk (Unhealthy)")
        else:
            results.append("Low Risk (Healthy)")
            
    return results

if __name__ == "__main__":
    try:
        model = load_model()
        print("Model loaded successfully!")
        print("You can import `predict_health` into your app script to serve predictions.")
    except Exception as e:
        print(f"Error: {e}")
