import pandas as pd

df = pd.read_csv('data/leg19_clean.csv')

# Count total number of MPs
total_mps = len(df)
print(f"Total number of MPs: {total_mps}")

# Count MPs with no education listed
null_education = df['titolo_studio'].isna().sum()
print(f"\nMPs with no education listed: {null_education} ({null_education/total_mps*100:.2f}%)")

# Get all unique education titles
all_education = []
for edu_str in df['titolo_studio'].dropna():
    edu_list = edu_str.strip('[]').split(',')
    edu_list = [edu.strip().strip("'") for edu in edu_list]
    all_education.extend(edu_list)
unique_education = set(all_education)
print(f"\nNumber of unique education titles: {len(unique_education)}")

# Count frequency of each education title
education_counts = pd.Series(all_education).value_counts()
print("\nTop 10 most common education titles:")
print(education_counts.head(10))

# Save detailed education analysis to CSV
education_analysis = pd.DataFrame({
    'education_title': education_counts.index,
    'count': education_counts.values,
    'percentage': (education_counts.values / total_mps * 100)
})
education_analysis.to_csv('results/education_analysis.csv', index=False)

# Create a distribution of number of education titles per MP
edu_count_per_mp = df['titolo_studio'].str.count(',') + 1
print("\nDistribution of number of education titles per MP:")
print(edu_count_per_mp.value_counts().sort_index())

# Function to categorize education titles into standardized groups
def categorize_education(education_text):
    if not isinstance(education_text, str):
        return "Unknown"
    
    education_text = education_text.lower()
    
    categories = {
        'laurea': ['laurea', 'dottore', 'dottorato', 'phd', 'master', 'specializzazione'],
        'diploma': ['diploma', 'maturità', 'liceo', 'istituto', 'scuola'],
        'certificate': ['certificato', 'attestato', 'qualifica'],
        'other': ['altro', 'altra', 'altri', 'altre']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in education_text:
                return category
    
    return "Other"

# Categorize education titles
df['education_category'] = df['titolo_studio'].apply(lambda x: [categorize_education(edu.strip().strip("'")) for edu in str(x).strip('[]').split(',')] if pd.notna(x) else ['Unknown'])

# Count frequency of each education category
education_category_counts = pd.Series([cat for cats in df['education_category'] for cat in cats]).value_counts()
print("\nDistribution of education categories:")
print(education_category_counts)

# Save education category analysis to CSV
education_category_analysis = pd.DataFrame({
    'education_category': education_category_counts.index,
    'count': education_category_counts.values,
    'percentage': (education_category_counts.values / total_mps * 100)
})
education_category_analysis.to_csv('results/education_category_analysis.csv', index=False) 