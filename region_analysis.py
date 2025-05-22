import pandas as pd
import os

def main():
    df = pd.read_csv('data/leg19_clean_with_regions.csv')
    
    null_count = df['regione_nascita'].isna().sum()
    if null_count > 0:
        print(f"Note: {null_count} MPs have missing region data and will be excluded from the analysis")
    
    region_counts = df['regione_nascita'].value_counts().reset_index()
    region_counts.columns = ['regione', 'absolute_count']
    
    total_mps = len(df) - null_count
    region_counts['percentage'] = region_counts['absolute_count'] / total_mps * 100
    
    region_counts = region_counts.sort_values('absolute_count', ascending=False)
    
    os.makedirs('results', exist_ok=True)
    region_counts.to_csv('results/region_analysis_summary.csv', index=False)
    print(f"Distribution data saved to 'results/region_analysis_summary.csv'")

if __name__ == "__main__":
    main() 