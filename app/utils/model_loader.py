import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../model/best_model.joblib")

def load_model():
    """Charge le modèle exporté par Camille (NB3)."""
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        return None