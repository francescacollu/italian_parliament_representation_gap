import pandas as pd
import os
from datetime import datetime

def analyze_gender_comparison(mp_df, pop_df, output_csv_path):
    """Compares gender distribution between MPs and general population."""
    # Process MP data
    mp_gender = mp_df['genere'].value_counts().reset_index()
    mp_gender.columns = ['gender', 'mp_count']
    total_mps = mp_gender['mp_count'].sum()
    mp_gender['mp_percentage'] = mp_gender['mp_count'] / total_mps
    
    # Process population data
    total_males = pop_df['Totale maschi'].sum()
    total_females = pop_df['Totale femmine'].sum()
    total_population = total_males + total_females
    
    pop_gender = pd.DataFrame({
        'gender': ['M', 'F'],
        'pop_count': [total_males, total_females],
        'pop_percentage': [total_males/total_population, total_females/total_population]
    })
    
    # Merge data
    comparison = pd.merge(mp_gender, pop_gender, on='gender', how='outer')
    
    # Calculate representation index
    comparison['representation_index'] = comparison['mp_percentage'] / comparison['pop_percentage']
    
    # Save results
    comparison.to_csv(output_csv_path, index=False)
    print(f"Gender comparison analysis saved to {output_csv_path}")

def analyze_age_comparison(mp_df, pop_df, output_csv_path):
    """Compares age distribution between MPs and general population."""
    # Calculate age for MPs
    mp_df['age'] = (datetime.now() - pd.to_datetime(mp_df['data_nascita'])).dt.total_seconds() / (365.25 * 24 * 60 * 60)
    
    # Create age groups
    age_bins = [0, 25, 35, 45, 55, 65, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    
    mp_df['age_group'] = pd.cut(mp_df['age'], bins=age_bins, labels=age_labels)
    
    # Process population data
    pop_df['Età'] = pd.to_numeric(pop_df['Età'], errors='coerce')
    pop_df['age_group'] = pd.cut(pop_df['Età'], bins=age_bins, labels=age_labels)
    
    # Calculate counts and percentages for MPs
    mp_age = mp_df['age_group'].value_counts().reset_index()
    mp_age.columns = ['age_group', 'mp_count']
    total_mps = mp_age['mp_count'].sum()
    mp_age['mp_percentage'] = mp_age['mp_count'] / total_mps
    
    # Calculate counts and percentages for population
    pop_age = pop_df.groupby('age_group')['Totale'].sum().reset_index()
    total_population = pop_age['Totale'].sum()
    pop_age['pop_percentage'] = pop_age['Totale'] / total_population
    pop_age = pop_age.rename(columns={'Totale': 'pop_count'})
    
    # Merge data
    comparison = pd.merge(mp_age, pop_age, on='age_group', how='outer')
    
    # Calculate representation index
    comparison['representation_index'] = comparison['mp_percentage'] / comparison['pop_percentage']
    
    # Sort by age group
    comparison = comparison.sort_values('age_group')
    
    # Save results
    comparison.to_csv(output_csv_path, index=False)
    print(f"Age comparison analysis saved to {output_csv_path}")

def analyze_region_comparison(mp_df, pop_df, pop_foreign_df, output_csv_path):
    """Compares regional distribution between MPs and general population."""

    mp_df['regione'] = mp_df['regione_nascita'].apply(clean_region_name)
    pop_df['regione'] = pop_df['Regione'].apply(clean_region_name)
    
    mp_region = mp_df['regione'].value_counts().reset_index()
    mp_region.columns = ['regione', 'mp_count']
    total_mps = mp_region['mp_count'].sum()
    mp_region['mp_percentage'] = mp_region['mp_count'] / total_mps

    mp_region = mp_region[mp_region['regione'] != 'Estero']
    
    pop_region = pop_df.groupby('regione')['Totale'].sum().reset_index()
    total_population = pop_region['Totale'].sum()
    pop_region['pop_percentage'] = pop_region['Totale'] / total_population
    pop_region = pop_region.rename(columns={'Totale': 'pop_count'})
    
    comparison = pd.merge(mp_region, pop_region, on='regione', how='outer')
    
    comparison['representation_index'] = comparison['mp_percentage'] / comparison['pop_percentage']
    
    comparison = comparison.sort_values('representation_index', ascending=False)
    
    comparison.to_csv(output_csv_path, index=False)
    print(f"Region comparison analysis saved to {output_csv_path}")

def clean_region_name(region_name):
    """Clean region names to match between datasets"""
    region_map = {
        "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste",
        "Trentino-Alto Adige": "Trentino-Alto Adige/Südtirol",
        "Friuli-Venezia Giulia": "Friuli-Venezia Giulia"
    }
    return region_map.get(region_name, region_name)

def analyze_foreign_comparison(mp_df, pop_foreign_df, output_csv_path):
    """Compares foreign distribution between MPs and general population."""
    foreign_total = pop_foreign_df[pop_foreign_df['Paese di nascita'] != 'Italia']['Totale'].sum()
    total_population = pop_foreign_df['Totale'].sum()
    foreign_row = pd.DataFrame({
        'regione': ['Estero'],
        'pop_count': [foreign_total],
        'pop_percentage': [foreign_total / (total_population + foreign_total)]
    })

    mp_region = mp_df['regione'].value_counts().reset_index()
    mp_region.columns = ['regione', 'mp_count']
    total_mps = mp_region['mp_count'].sum()
    mp_region['mp_percentage'] = mp_region['mp_count'] / total_mps

    mp_region = mp_region[mp_region['regione'] == 'Estero']

    comparison = pd.merge(mp_region, foreign_row, on='regione', how='outer')

    comparison.to_csv(output_csv_path, index=False)
    print(f"Foreign comparison analysis saved to {output_csv_path}")    

    

def main():
    mp_df = pd.read_csv('data/leg19_clean_with_regions.csv')
    pop_df = pd.read_csv('data/pop_residente_1gen2025.csv')
    pop_region_df = pd.read_csv('data/pop_residente_1gen2025_regioni.csv')
    pop_foreign_df = pd.read_csv('data/pop_birth_foreign_countries_1gen2024.csv')
    
    os.makedirs('results', exist_ok=True)
    
    #analyze_gender_comparison(mp_df, pop_df, 'results/gender_comparison_analysis.csv')
    #analyze_age_comparison(mp_df, pop_df, 'results/age_comparison_analysis.csv')
    analyze_region_comparison(mp_df, pop_region_df, pop_foreign_df, 'results/region_comparison_analysis.csv')
    analyze_foreign_comparison(mp_df, pop_foreign_df, 'results/foreign_comparison_analysis.csv')

if __name__ == "__main__":
    main() 