import pandas as pd
import numpy as np
import ast

def clean_name(name):
    """Clean name by removing extra spaces and converting to lowercase"""
    return ' '.join(name.lower().split())

def main():
    # Read the main dataset
    df_main = pd.read_csv('data/leg19_clean.csv')
    
    # Fill education based on profession
    profession_education_map = {
        'Avvocato': 'Laurea in Giurisprudenza',
        'Medico': 'Laurea in Medicina'
    }
    
    # Count null values before update
    null_before = df_main['titolo_studio'].isna().sum()
    
    # Update education based on profession
    for idx, row in df_main.iterrows():
        if pd.isna(row['titolo_studio']):
            try:
                professions = ast.literal_eval(row['professione'])
                for profession in professions:
                    if profession in profession_education_map:
                        df_main.at[idx, 'titolo_studio'] = profession_education_map[profession]
                        break
            except (ValueError, SyntaxError):
                continue
    
    # Count updates from profession
    profession_updates = null_before - df_main['titolo_studio'].isna().sum()
    
    # Read the Wikipedia education data
    df_wiki = pd.read_csv('results/wikipedia_education.csv')
    
    # Clean names in both datasets for comparison
    df_main['nome_clean'] = df_main['nome'].apply(clean_name)
    df_main['cognome_clean'] = df_main['cognome'].apply(clean_name)
    df_wiki['nome_clean'] = df_wiki['nome'].apply(clean_name)
    df_wiki['cognome_clean'] = df_wiki['cognome'].apply(clean_name)
    
    # Create a dictionary of Wikipedia education data
    wiki_education = {}
    for _, row in df_wiki.iterrows():
        key = (row['nome_clean'], row['cognome_clean'])
        if key not in wiki_education:
            wiki_education[key] = row['titolo_studio']
    
    # Update education for MPs with null titolo_studio
    wiki_updates = 0
    for idx, row in df_main.iterrows():
        if pd.isna(row['titolo_studio']):
            key = (row['nome_clean'], row['cognome_clean'])
            if key in wiki_education:
                df_main.at[idx, 'titolo_studio'] = wiki_education[key]
                wiki_updates += 1
    
    # Save the updated dataset
    df_main = df_main.drop(['nome_clean', 'cognome_clean'], axis=1)
    df_main.to_csv('data/leg19_clean_updated.csv', index=False)
    
    print(f"Updated {profession_updates} records based on profession")
    print(f"Updated {wiki_updates} records with Wikipedia education data")
    print(f"Total records in dataset: {len(df_main)}")
    print(f"Records with null titolo_studio before any update: {null_before}")
    print(f"Records with null titolo_studio after all updates: {df_main['titolo_studio'].isna().sum()}")

if __name__ == "__main__":
    main() 