import pandas as pd
import os

def analyze_general_education(df, pop_general_education, output_csv_path):
    df['titolo_studio'] = df['titolo_studio'].fillna('not specified').str.lower()

    licenza_elementare = df['titolo_studio'].str.contains('licenza elementare').sum()
    licenza_media = df['titolo_studio'].str.contains('licenza media').sum()
    diploma = df['titolo_studio'].str.contains('diploma').sum()
    laurea = df['titolo_studio'].str.contains('laurea').sum()
    total = len(df)

    general_education = pd.DataFrame({
        'massimo_titolo_studio': ['Licenza Media', 'Diploma', 'Laurea'],
        'mp_count': [licenza_elementare+licenza_media, diploma, laurea],
        'mp_percentage': [(licenza_elementare+licenza_media)/total, diploma/total, laurea/total]
    })

    comparison = pd.merge(general_education, pop_general_education, on='massimo_titolo_studio', how='outer')
    comparison['representation_index'] = comparison['mp_percentage'] / comparison['pop_percentage']

    os.makedirs('results', exist_ok=True)
    comparison.to_csv(output_csv_path, index=False)
    print(f"Distribution data saved to " + output_csv_path)

def analyze_university_education(df, laureati_pop2022, output_csv_path):
    df['titolo_studio'] = df['titolo_studio'].fillna('not specified').str.lower()
    excluded_values = ['na', 'diploma', 'licenza elementare', 'licenza media']
    df_laureati = df[~df['titolo_studio'].str.contains('|'.join(excluded_values), case=False, na=False)]

    mp_counts = df_laureati['gruppo_laurea'].value_counts()
    total_laureati = len(df_laureati)
    
    mp_education = pd.DataFrame({
        'gruppo_laurea': mp_counts.index,
        'mp_count': mp_counts.values,
        'mp_percentage': mp_counts.values / total_laureati
    })

    comparison = pd.merge(mp_education, laureati_pop2022, on='gruppo_laurea', how='outer')

    comparison['mp_count'] = comparison['mp_count'].fillna(0)
    comparison['mp_percentage'] = comparison['mp_percentage'].fillna(0)

    comparison['representation_index'] = comparison['mp_percentage'] / comparison['pop_percentage']

    comparison = comparison.sort_values('mp_count', ascending=False)

    os.makedirs('results', exist_ok=True)
    comparison.to_csv(output_csv_path, index=False)
    print(f"University education distribution data saved to {output_csv_path}")

def main():
    df = pd.read_csv('data/leg19_clean_updated.csv')

    pop_general_education = pd.read_csv('data/pop_general_education.csv')
    laureati_pop2022 = pd.read_csv('data/laureati_pop2022.csv')

    analyze_general_education(df, pop_general_education,'results/general_education_analysis.csv')
    analyze_university_education(df, laureati_pop2022, 'results/university_education_analysis.csv')

if __name__ == "__main__":
    main() 