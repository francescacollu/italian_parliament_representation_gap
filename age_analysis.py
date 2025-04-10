import pandas as pd
import plotly.express as px

df = pd.read_csv('data/leg19_clean.csv')

def analyze_age(dataframe, output_csv_path):
    """Calculates counts and percentages of MPs under 35 and over 70 years old and saves to CSV."""
    # Convert data_nascita to datetime
    dataframe['data_nascita'] = pd.to_datetime(dataframe['data_nascita'])

    # Calculate age
    today = pd.Timestamp.now()
    dataframe['age'] = (today - dataframe['data_nascita']).dt.total_seconds() / (365.25 * 24 * 60 * 60)

    # Define age groups
    under_35 = dataframe[dataframe['age'] < 35]
    over_70 = dataframe[dataframe['age'] > 70]

    # Calculate counts
    under_35_count = len(under_35)
    over_70_count = len(over_70)

    # Calculate percentages
    under_35_percentage = (under_35_count / len(dataframe)) * 100
    over_70_percentage = (over_70_count / len(dataframe)) * 100

    # Create summary DataFrame
    age_summary = pd.DataFrame({
        'age_group': ['Under 35', 'Over 70'],
        'absolute_count': [under_35_count, over_70_count],
        'percentage': [under_35_percentage, over_70_percentage]
    })

    print("Age Analysis Summary:")
    print(age_summary)

    age_summary.to_csv(output_csv_path, index=False)
    print(f"Age analysis saved to {output_csv_path}")

# Run the analysis
analyze_age(df, 'results/age_analysis_summary.csv')

