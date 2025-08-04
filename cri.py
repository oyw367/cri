import pandas as pd
import matplotlib.dates as mdates
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
import sys
import os
import numpy as np
from tzlocal import get_localzone

class Processor:
    EXPECTED_COLUMNS = ['Patient ID', 'Age', 'Sex', 'Smoking', 'Brushing', 
                        'Plaque index baseline (Monthly change)', 'Pocket Depth(mm) baseline (Monthly change)', 
                        'BOP(%) baseline (Monthly change)', 'General condition', 'Label']
    
    def __init__(self):
        self.data = None
    def load_data(self, filepath):
        filepath = 'gingivitis.csv'
        try:
            self.data = pd.read_csv(filepath)
            self.data.columns = self.EXPECTED_COLUMNS
        except Exception as e:
            print(f'Warning: files missing{e}')
            sys.exit(1)

    def clean_symptoms(self):
        df = self.data
        df['General condition'] = df['General condition'].fillna('N/A')
        maps = {
            'Sex': {'M': 1, 'F': 0},
            'Smoking': {'Yes': 1, 'No': 0},
            'Brushing': {'poor': 0, 'fair': 1, 'good': 2},
            'General condition': {
                'Hypertension': 0,
                'Diabetes Mellitus': 1,
                'Asthma': 2,
                'Hyperlipidemia': 3,
                'N/A': None
            },
            'Label': {'Severe': 1, 'Non-severe': 0}
        }
        for col, m in maps.items():
            unmapped = set(df[col].dropna().unique()) - set(m.keys())
            if unmapped:
                raise ValueError(f"Unexpected values in {col}: {unmapped}")
            df[col] = df[col].map(m)

        # helper to split time series columns
        def split_monthly(col_name: str, prefix: str):
            parts = df[col_name].str.split('=>', expand=True)
            if parts.shape[1] != 3:
                raise ValueError(f"{col_name} should split into 3 parts, got {parts.shape[1]}")
            df[[f"{prefix}_m1", f"{prefix}_m2", f"{prefix}_m3"]] = parts.astype(float)
        self.data = df
        split_monthly('Plaque index baseline (Monthly change)', 'plaque')
        split_monthly('Pocket Depth(mm) baseline (Monthly change)', 'pd')
        split_monthly('BOP(%) baseline (Monthly change)', 'BOP')

        self.data = df  # update in place


    

if __name__ == "__main__":

    analyzer = Processor()
    analyzer.load_data('gingivitis.csv')  
    analyzer.clean_symptoms() 
    # after calling analyzer.clean_symptoms()
    analyzer.data.to_csv('gingivitis.cleaned.csv', index=False)















    
    

