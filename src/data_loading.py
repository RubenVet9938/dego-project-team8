import json
import pandas as pd

def load_raw_data(path="../data/raw_credit_applications.json"):
    """Load and flatten the raw credit applications JSON into a DataFrame."""
    with open(path) as f:
        data = json.load(f)
    return pd.json_normalize(data)
