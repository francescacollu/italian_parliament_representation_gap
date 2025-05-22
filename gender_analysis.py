import pandas as pd

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

analyze_gender(df, 'results/gender_analysis_summary.csv')

