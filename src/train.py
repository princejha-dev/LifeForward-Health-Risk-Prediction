import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, recall_score

def train_model():
    print("Loading data...")
    # Load dataset assuming the script is run from the project root
    data_path = "dataset/novagen_dataset.csv"
    if not os.path.exists(data_path):
        data_path = "../dataset/novagen_dataset.csv" # fallback if run from src/
        
    df = pd.read_csv(data_path)

    X = df.drop("Target", axis=1)
    y = df["Target"]

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # From Notebook: Random Forest was the best model (95.8% Recall)
    print("Training Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42
    )

    rf.fit(X_train, y_train)

    print("Evaluating Model...")
    y_pred = rf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred):.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save format
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "health_model.pkl")
    
    joblib.dump(rf, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_model()
