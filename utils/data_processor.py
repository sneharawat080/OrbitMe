import pandas as pd
import os

def ensure_data_directory():
    """Ensure data directory exists"""
    os.makedirs('./data', exist_ok=True)

def load_health_data():
    """Load health data with error handling"""
    try:
        if os.path.exists('./data/health_data.csv'):
            return pd.read_csv('./data/health_data.csv')
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading health data: {e}")
        return pd.DataFrame()

def load_work_data():
    """Load work data with error handling"""
    try:
        if os.path.exists('./data/work_data.csv'):
            return pd.read_csv('./data/work_data.csv')
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading work data: {e}")
        return pd.DataFrame()