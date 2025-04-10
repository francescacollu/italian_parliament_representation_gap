import pandas as pd

# Read the data
df = pd.read_csv('data/leg19_clean.csv')

# Find MPs with missing profession (empty list, None, or "Professione Non Rilevata")
missing_profession = df[
    (df['professione'] == "['']") |
    (df['professione'] == '[None]') |
    (df['professione'] == "['Professione Non Rilevata']")
]

# Create a DataFrame with just the names of MPs with missing profession
missing_profession_names = missing_profession[['nome', 'cognome']]

# Sort by last name, then first name
missing_profession_names = missing_profession_names.sort_values(['cognome', 'nome'])

# Print the results
print(f"Number of MPs with missing profession: {len(missing_profession_names)}")
print("\nList of MPs with missing profession:")
print(missing_profession_names.to_string(index=False))

# Save to CSV
missing_profession_names.to_csv('results/missing_profession_mp.csv', index=False)
print("\nResults saved to results/missing_profession_mp.csv")