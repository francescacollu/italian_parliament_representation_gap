import pandas as pd
import plotly.express as px

df = pd.read_csv('data/pop_residente_1gen2025.csv')

def analyze_gender(dataframe, output_csv_path):
    """Calculates gender counts and percentages and saves to CSV."""
    # Get total counts for males and females
    total_males = dataframe['Totale maschi'].sum()
    total_females = dataframe['Totale femmine'].sum()
    total_population = total_males + total_females

    # Calculate percentages
    male_percentage = (total_males / total_population) * 100
    female_percentage = (total_females / total_population) * 100

    # Create summary DataFrame
    gender_summary = pd.DataFrame({
        'genere': ['M', 'F'],
        'absolute_count': [total_males, total_females],
        'percentage': [male_percentage, female_percentage]
    })

    print("Gender Analysis Summary:")
    print(gender_summary)

    gender_summary.to_csv(output_csv_path, index=False)
    print(f"Gender analysis saved to {output_csv_path}")

def analyze_age(dataframe, output_csv_path):
    """Calculates counts and percentages of people under 35 and over 70 years old and saves to CSV."""
    # Convert 'Età' to numeric, handling '100 e oltre' and 'Totale'
    dataframe['Età'] = dataframe['Età'].replace('100 e oltre', 100)
    # Remove the 'Totale' row before converting to numeric
    dataframe = dataframe[dataframe['Età'] != 'Totale']
    dataframe['Età'] = pd.to_numeric(dataframe['Età'])

    # Define age groups
    under_35 = dataframe[dataframe['Età'] < 35]
    over_70 = dataframe[dataframe['Età'] > 70]

    # Calculate counts
    under_35_count = under_35['Totale'].sum()
    over_70_count = over_70['Totale'].sum()
    total_population = dataframe['Totale'].sum()

    # Calculate percentages
    under_35_percentage = (under_35_count / total_population) * 100
    over_70_percentage = (over_70_count / total_population) * 100

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

# Run the analyses
analyze_gender(df, 'results/population_gender_analysis_summary.csv')
analyze_age(df, 'results/population_age_analysis_summary.csv')
