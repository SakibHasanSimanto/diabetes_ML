# model/predictor.py
import pickle, numpy as np, os, warnings
warnings.filterwarnings("ignore", category=UserWarning)   # optional – hides the version notice

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../dt_diabetes_model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

def _risk_band(p):
    """Map probability to a label & quick advice."""
    if p < 0.60:
        return "Low",      "Keep up a balanced diet and regular exercise."
    elif p < 0.80:
        return "Moderate", "Consider a routine check‑up and review lifestyle habits."
    else:
        return "High",     "See a healthcare professional for diagnostic testing soon."

def predict_diabetes(input_data):
    """
    Returns: result_str, prob_float, risk_band_str, advice_str
    """
    arr = np.array(input_data).reshape(1, -1)
    prob = model.predict_proba(arr)[0][1]        # probability of class “1” (at‑risk)
    result = "At Risk" if prob >= 0.50 else "Not At Risk"
    band, advice = _risk_band(prob)
    return result, round(prob, 2), band, advice
