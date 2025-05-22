import pandas as pd
import plotly.express as px
import os
from datetime import datetime

def analyze_age(df, output_csv_path):
    """Calculates counts and percentages of MPs under 35 and over 70 years old and saves to CSV."""

    df['data_nascita'] = pd.to_datetime(df['data_nascita'])

    today = pd.Timestamp.now()
    df['age'] = (today - df['data_nascita']).dt.total_seconds() / (365.25 * 24 * 60 * 60)

    under_35 = df[df['age'] < 35]
    over_70 = df[df['age'] > 70]

    under_35_count = len(under_35)
    over_70_count = len(over_70)

    under_35_percentage = (under_35_count / len(df))
    over_70_percentage = (over_70_count / len(df)) 

    age_summary = pd.DataFrame({
        'age_group': ['Under 35', 'Over 70'],
        'absolute_count': [under_35_count, over_70_count],
        'percentage': [under_35_percentage, over_70_percentage]
    })

    print("Age Analysis Summary:")
    print(age_summary)

    age_summary.to_csv(output_csv_path, index=False)
    print(f"Age analysis saved to {output_csv_path}")

def analyze_age_comparison(mp_df, pop_df, output_csv_path):
    """Compares age distribution between MPs and general population."""

    mp_df['age'] = (datetime.now() - pd.to_datetime(mp_df['data_nascita'])).dt.total_seconds() / (365.25 * 24 * 60 * 60)
    
    age_bins = [0, 25, 35, 45, 55, 65, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    
    mp_df['age_group'] = pd.cut(mp_df['age'], bins=age_bins, labels=age_labels)
    
    # Process population data
    pop_df['Età'] = pd.to_numeric(pop_df['Età'], errors='coerce')
    pop_df['age_group'] = pd.cut(pop_df['Età'], bins=age_bins, labels=age_labels)
    
    mp_age = mp_df['age_group'].value_counts().reset_index()
    mp_age.columns = ['age_group', 'mp_count']
    total_mps = mp_age['mp_count'].sum()
    mp_age['mp_percentage'] = mp_age['mp_count'] / total_mps
    
    pop_age = pop_df.groupby('age_group')['Totale'].sum().reset_index()
    total_population = pop_age['Totale'].sum()
    pop_age['pop_percentage'] = pop_age['Totale'] / total_population
    pop_age = pop_age.rename(columns={'Totale': 'pop_count'})
    
    comparison = pd.merge(mp_age, pop_age, on='age_group', how='outer')
    
    comparison['representation_index'] = comparison['mp_percentage'] / comparison['pop_percentage']
    
    comparison = comparison.sort_values('age_group')
    
    comparison.to_csv(output_csv_path, index=False)
    print(f"Age comparison analysis saved to {output_csv_path}")

def main():
    df = pd.read_csv('data/leg19_clean_updated.csv')
    pop_df = pd.read_csv('data/pop_residente_1gen2025.csv')

    os.makedirs('results', exist_ok=True)

    analyze_age(df, 'results/age_analysis_summary.csv')
    analyze_age_comparison(df, pop_df, 'results/age_comparison_analysis.csv')

if __name__ == "__main__":
    main()

