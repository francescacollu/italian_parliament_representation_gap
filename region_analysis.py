import pandas as pd
import os

def analyze_regions(df, output_csv_path):    
    null_count = df['regione_nascita'].isna().sum()
    if null_count > 0:
        print(f"Note: {null_count} MPs have missing region data and will be excluded from the analysis")
    
    region_counts = df['regione_nascita'].value_counts().reset_index()
    region_counts.columns = ['regione', 'absolute_count']
    
    total_mps = len(df) - null_count
    region_counts['percentage'] = region_counts['absolute_count'] / total_mps * 100
    
    region_counts = region_counts.sort_values('absolute_count', ascending=False)
    
    region_counts.to_csv(output_csv_path, index=False)
    print(f"Distribution data saved to {output_csv_path}")

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
    
    analyze_region_comparison(mp_df, pop_region_df, pop_foreign_df, 'results/region_comparison_analysis.csv')
    analyze_foreign_comparison(mp_df, pop_foreign_df, 'results/foreign_comparison_analysis.csv')

if __name__ == "__main__":
    main() 