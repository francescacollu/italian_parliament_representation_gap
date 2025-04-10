import pandas as pd
import re

df = pd.read_csv('data/leg19_clean.csv')

# Count total number of MPs
total_mps = len(df)
print(f"Total number of MPs: {total_mps}")

# Get all unique professions
all_professions = []
for prof_str in df['professione']:
    prof_list = prof_str.strip('[]').split(',')
    prof_list = [prof.strip().strip("'") for prof in prof_list]
    all_professions.extend(prof_list)
unique_professions = set(all_professions)
print(f"\nNumber of unique professions: {len(unique_professions)}")

# Count frequency of each profession
profession_counts = pd.Series(all_professions).value_counts()
print("\nTop 10 most common professions:")
print(profession_counts.head(10))

# Save detailed profession analysis to CSV
profession_analysis = pd.DataFrame({
    'profession': profession_counts.index,
    'count': profession_counts.values,
    'percentage': (profession_counts.values / total_mps * 100)
})
profession_analysis.to_csv('results/profession_analysis.csv', index=False)

# Create a histogram of number of professions per MP
prof_count_per_mp = df['professione'].str.count(',') + 1
print("\nDistribution of number of professions per MP:")
print(prof_count_per_mp.value_counts().sort_index())

# Function to categorize professions into standardized groups
def categorize_profession(profession_text):
    if not isinstance(profession_text, str):
        return "Unknown"
    
    profession_text = profession_text.lower()
    
    categories = {
        'lawyer': ['avvocato', 'giurista', 'penalista', 'civilista', 'amministrativista', 'diritto'],
        'professor': ['professor', 'docente', 'insegnante', 'ricercatore', 'accadem'],
        'entrepreneur': ['imprendit', 'industriale'],
        'manager': ['manager', 'dirigente', 'direttore', 'amministratore'],
        'doctor': ['medico', 'chirurgo', 'odontoiatra', 'sanitario'],
        'public_employee': ['funzionario', 'dipendente pubblic', 'dipendente di azienda pubblica', 'impiegato pubblic'],
        'private_employee': ['dipendente di azienda privata', 'impiegato', 'dipendente'],
        'consultant': ['consulente'],
        'journalist': ['giornalista'],
        'engineer': ['ingegner'],
        'accountant': ['commercialista', 'ragioniere', 'revisore', 'contabil'],
        'politician': ['sindac', 'consigliere', 'parlamentare', 'assessore', 'politico', 'amministratore locale'],
        'banker': ['bancario', 'banc'],
        'union_member': ['sindacalista'],
        'economist': ['econom'],
        'law_enforcement': ['polizia', 'forze dell\'ordine', 'sicurezza'],
        'architect': ['architetto'],
        'farmer': ['agricol', 'agrar'],
        'artist': ['artist', 'musici', 'attore']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in profession_text:
                return category
    
    return "Other"

# Categorize professions
df['profession_category'] = df['professione'].apply(lambda x: [categorize_profession(prof.strip().strip("'")) for prof in x.strip('[]').split(',')])

# Count frequency of each profession category
profession_category_counts = pd.Series([cat for cats in df['profession_category'] for cat in cats]).value_counts()
print("\nDistribution of profession categories:")
print(profession_category_counts)

# Save profession category analysis to CSV
profession_category_analysis = pd.DataFrame({
    'profession_category': profession_category_counts.index,
    'count': profession_category_counts.values,
    'percentage': (profession_category_counts.values / total_mps * 100)
})
profession_category_analysis.to_csv('results/profession_category_analysis.csv', index=False)