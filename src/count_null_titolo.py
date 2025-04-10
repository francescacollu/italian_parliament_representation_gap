import pandas as pd

# Read the dataset
df = pd.read_csv('data/leg19_clean.csv')

# Count null values
null_count = df['titolo_studio'].isna().sum()
total_count = len(df)

print(f"Total number of MPs: {total_count}")
print(f"Number of MPs with null titolo_studio: {null_count}")
print(f"Percentage of MPs with null titolo_studio: {(null_count/total_count)*100:.2f}%")

# Show a few examples of MPs with null titolo_studio
print("\nExample MPs with null titolo_studio:")
print(df[df['titolo_studio'].isna()][['nome', 'cognome']].head()) 