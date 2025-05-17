import pandas as pd
import os
import plotly.express as px

def main():
    # Read population data
    pop_df = pd.read_csv('data/pop_residente_1gen2025_regioni.csv')
    
    # Process population data
    pop_analysis = pop_df[['Regione', 'Totale']].copy()
    pop_analysis.columns = ['regione', 'population']
    
    # Calculate percentage
    total_population = pop_analysis['population'].sum()
    pop_analysis['percentage'] = pop_analysis['population'] / total_population * 100
    
    # Sort by population descending
    pop_analysis = pop_analysis.sort_values('population', ascending=False)
    
    # Save to CSV
    os.makedirs('results', exist_ok=True)
    pop_analysis.to_csv('results/population_regions_analysis_summary.csv', index=False)
    print(f"Population analysis saved to 'results/population_regions_analysis_summary.csv'")
    
    # Read MP data to compare
    mp_df = pd.read_csv('data/leg19_clean_with_regions.csv')
    
    # Calculate MP distribution
    mp_counts = mp_df['regione_nascita'].value_counts().reset_index()
    mp_counts.columns = ['regione', 'mp_count']
    
    # Clean region names to match population data
    mp_counts['regione'] = mp_counts['regione'].apply(clean_region_name)
    
    # Remove 'Estero' for comparison with Italian regions
    mp_counts = mp_counts[mp_counts['regione'] != 'Estero']
    
    # Merge data for comparison
    comparison = pd.merge(pop_analysis, mp_counts, on='regione', how='left')
    comparison['mp_count'] = comparison['mp_count'].fillna(0).astype(int)
    
    # Calculate MP percentage and expected representation
    total_mps = comparison['mp_count'].sum()
    comparison['mp_percentage'] = comparison['mp_count'] / total_mps * 100
    
    # Calculate expected number of MPs based on population
    comparison['expected_mps'] = total_mps * comparison['percentage'] / 100
    
    # Calculate representation index (actual/expected)
    comparison['representation_index'] = comparison['mp_count'] / comparison['expected_mps']
    
    # Save comparative analysis
    comparison.to_csv('results/region_representation_analysis.csv', index=False)
    print(f"Representation analysis saved to 'results/region_representation_analysis.csv'")
    
    # Create visualization
    fig = px.bar(
        comparison,
        y='regione',
        x=['representation_index'],
        title='Regional Representation Index (1.0 = perfect representation)',
        labels={'value': 'Representation Index', 'regione': 'Region'},
        height=700,
        orientation='h'
    )
    
    # Add a vertical line at 1.0 (perfect representation)
    fig.add_vline(x=1.0, line_dash="dash", line_color="red")
    
    # Update layout
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.write_html('results/region_representation_index.html')
    print(f"Representation index visualization saved to 'results/region_representation_index.html'")
    
    # Print summary statistics
    print("\nPopulation Distribution Summary:")
    print(f"Total Italian population: {total_population:,}")
    print("\nTop 5 populated regions:")
    print(pop_analysis.head(5)[['regione', 'population', 'percentage']].to_string(index=False))
    
    print("\nBottom 5 populated regions:")
    print(pop_analysis.tail(5)[['regione', 'population', 'percentage']].to_string(index=False))
    
    # Print comparative analysis
    print("\nMost over-represented regions (representation index > 1.2):")
    over_represented = comparison[comparison['representation_index'] > 1.2].sort_values('representation_index', ascending=False)
    if len(over_represented) > 0:
        print(over_represented[['regione', 'representation_index', 'mp_count', 'expected_mps']].to_string(index=False))
    else:
        print("None")
    
    print("\nMost under-represented regions (representation index < 0.8):")
    under_represented = comparison[comparison['representation_index'] < 0.8].sort_values('representation_index')
    if len(under_represented) > 0:
        print(under_represented[['regione', 'representation_index', 'mp_count', 'expected_mps']].to_string(index=False))
    else:
        print("None")

def clean_region_name(region_name):
    """Clean region names to match between datasets"""
    # Mapping of region names between datasets
    region_map = {
        "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste",
        "Trentino-Alto Adige": "Trentino-Alto Adige/Südtirol",
        "Friuli-Venezia Giulia": "Friuli-Venezia Giulia"
    }
    
    # Return the mapped name if available, otherwise return the original
    return region_map.get(region_name, region_name)

if __name__ == "__main__":
    main() 