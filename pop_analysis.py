import pandas as pd

df = pd.read_csv('data/pop_residente_1gen2025.csv')
df_regions = pd.read_csv('data/pop_residente_1gen2025_regioni.csv')
df_birth_countries = pd.read_csv('data/pop_birth_foreign_countries_1gen2024.csv')

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

def analyze_regions(dataframe, output_csv_path):
    """Calculates regional population counts and percentages and saves to CSV."""
    # Process regional data
    region_analysis = dataframe[['Regione', 'Totale']].copy()
    region_analysis.columns = ['regione', 'absolute_count']
    
    # Calculate percentage
    total_population = region_analysis['absolute_count'].sum()
    region_analysis['percentage'] = region_analysis['absolute_count'] / total_population * 100
    
    # Sort by population descending
    region_analysis = region_analysis.sort_values('absolute_count', ascending=False)
    
    print("Region Analysis Summary:")
    print(f"Total population: {total_population:,}")
    print("\nTop 5 populated regions:")
    print(region_analysis.head(5))
    
    print("\nBottom 5 populated regions:")
    print(region_analysis.tail(5))
    
    # Save to CSV
    region_analysis.to_csv(output_csv_path, index=False)
    print(f"Region analysis saved to {output_csv_path}")

def analyze_birth_place(dataframe, output_csv_path):
    """Calculates population counts by birth place (Italy vs. foreign) and saves to CSV."""
    # Get count for people born in Italy
    italy_born = dataframe[dataframe['Paese di nascita'] == 'Italia']['Totale'].iloc[0]
    
    # Calculate count for people born in foreign countries (total minus Italy)
    total_population = dataframe['Totale'].sum()
    foreign_born = total_population - italy_born
    
    # Create summary DataFrame
    birth_place_summary = pd.DataFrame({
        'nascita': ['Italia', 'Estero'],
        'absolute_count': [italy_born, foreign_born],
        'percentage': [(italy_born / total_population) * 100, (foreign_born / total_population) * 100]
    })
    
    print("Birth Place Analysis Summary:")
    print(f"Total population: {total_population:,}")
    print(birth_place_summary)
    
    # Save to CSV
    birth_place_summary.to_csv(output_csv_path, index=False)
    print(f"Birth place analysis saved to {output_csv_path}")

# Run the analyses
analyze_gender(df, 'results/population_gender_analysis_summary.csv')
analyze_age(df, 'results/population_age_analysis_summary.csv')
analyze_regions(df_regions, 'results/population_regions_analysis_summary.csv')
analyze_birth_place(df_birth_countries, 'results/population_birth_place_analysis_summary.csv')
