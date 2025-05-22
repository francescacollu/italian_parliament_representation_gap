import pandas as pd
import os

df = pd.read_csv('data/leg19_clean_updated.csv')

def analyze_gender(dataframe, output_csv_path):
    """Calculates gender counts and percentages and saves to CSV."""
    gender_counts = dataframe['genere'].value_counts().reset_index()
    gender_counts.columns = ['genere', 'absolute_count']

    gender_percentages = dataframe['genere'].value_counts(normalize=True).reset_index()
    gender_percentages.columns = ['genere', 'percentage']
    gender_percentages['percentage'] = gender_percentages['percentage'] * 100

    gender_summary = pd.merge(gender_counts, gender_percentages, on='genere')

    print("Gender Analysis Summary:")
    print(gender_summary)

    gender_summary.to_csv(output_csv_path, index=False)
    print(f"Gender analysis saved to {output_csv_path}")

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


def main():
    mp_df = pd.read_csv('data/leg19_clean_updated.csv')
    pop_df = pd.read_csv('data/pop_residente_1gen2025.csv')

    os.makedirs('results', exist_ok=True)

    analyze_gender(df, 'results/gender_analysis_summary.csv')
    analyze_gender_comparison(mp_df, pop_df, 'results/gender_comparison_analysis.csv')

if __name__ == "__main__":
    main()

