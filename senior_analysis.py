import pandas as pd
import plotly.express as px
from datetime import datetime

# Read the data
camera_df = pd.read_csv('data/Camera_Leg19.csv')
senato_df = pd.read_csv('data/Senato_Leg19.csv')

# Function to calculate age
def calculate_age(birthdate, current_date=None):
    if current_date is None:
        current_date = datetime.now()
        
    if isinstance(birthdate, str):
        # Try different formats for Camera data
        try:
            # Format YYYYMMDD (like "19850520")
            birth = datetime.strptime(birthdate, '%Y%m%d')
        except ValueError:
            try:
                # Format YYYY-MM-DD
                birth = datetime.strptime(birthdate, '%Y-%m-%d')
            except ValueError:
                return None
    else:
        # For non-string dates (already parsed)
        birth = birthdate
        
    age = current_date.year - birth.year - ((current_date.month, current_date.day) < (birth.month, birth.day))
    return age

# Get unique members for Camera
camera_members = camera_df[['persona', 'cognome', 'nome', 'genere', 'dataNascita']].drop_duplicates()

# Camera: Convert birth dates and calculate ages
# In Camera dataset, dataNascita seems to be in format YYYYMMDD as a string
camera_members['birth_date'] = pd.to_datetime(camera_members['dataNascita'], format='%Y%m%d', errors='coerce')
camera_members['age'] = camera_members['birth_date'].apply(lambda x: calculate_age(x) if pd.notna(x) else None)

# Get unique members for Senato
senato_members = senato_df[['senatore', 'cognome', 'nome', 'genere', 'dataNascita']].drop_duplicates()

# Senato: Convert birth dates and calculate ages
# In Senato dataset, dataNascita seems to be in format YYYY-MM-DD
senato_members['birth_date'] = pd.to_datetime(senato_members['dataNascita'], errors='coerce')
senato_members['age'] = senato_members['birth_date'].apply(lambda x: calculate_age(x) if pd.notna(x) else None)

# Filter for members 70 years old or older
senior_camera = camera_members[camera_members['age'] >= 70].copy()
senior_senato = senato_members[senato_members['age'] >= 70].copy()

# Add chamber information
senior_camera['chamber'] = 'Camera'
senior_senato['chamber'] = 'Senato'

# Combine results
all_seniors = pd.concat([
    senior_camera[['nome', 'cognome', 'genere', 'age', 'chamber']], 
    senior_senato[['nome', 'cognome', 'genere', 'age', 'chamber']]
])

# Print results
print("\nMembers of Parliament 70 years old or older:")
if len(all_seniors) > 0:
    print(all_seniors.sort_values(by=['age'], ascending=False).head(10))  # Show top 10 oldest
    print(f"\nTotal senior members: {len(all_seniors)}")
    print(f"Senior members in Camera: {len(senior_camera)}")
    print(f"Senior members in Senato: {len(senior_senato)}")
    
    # Gender distribution among senior members
    senior_gender_counts = all_seniors['genere'].value_counts()
    print("\nGender distribution among senior members:")
    print(senior_gender_counts)
    
    # Age distribution among senior members
    age_counts = all_seniors['age'].value_counts().sort_index()
    print("\nAge distribution among senior members (showing ranges):")
    age_ranges = {
        '70-74': all_seniors[(all_seniors['age'] >= 70) & (all_seniors['age'] <= 74)].shape[0],
        '75-79': all_seniors[(all_seniors['age'] >= 75) & (all_seniors['age'] <= 79)].shape[0],
        '80-84': all_seniors[(all_seniors['age'] >= 80) & (all_seniors['age'] <= 84)].shape[0],
        '85+': all_seniors[all_seniors['age'] >= 85].shape[0]
    }
    for range_name, count in age_ranges.items():
        print(f"{range_name}: {count}")
    
    # Create visualizations
    
    # Gender distribution pie chart
    # Handle different gender encodings in the two datasets
    gender_data = []
    for gender, count in senior_gender_counts.items():
        if gender in ['male', 'M']:
            gender_data.append({'Gender': 'Men', 'Count': count})
        elif gender in ['female', 'F']:
            gender_data.append({'Gender': 'Women', 'Count': count})
    
    gender_df = pd.DataFrame(gender_data)
    
    fig1 = px.pie(
        gender_df, 
        values='Count',
        names='Gender',
        title='Gender Distribution Among MPs 70 or Older',
        color='Gender',
        color_discrete_map={'Men': '#0066CC', 'Women': '#FF69B4'}
    )
    fig1.update_traces(textinfo='percent+value')
    fig1.write_html('senior_gender_distribution.html')
    
    # Age distribution bar chart
    age_range_df = pd.DataFrame({
        'Age Range': list(age_ranges.keys()),
        'Count': list(age_ranges.values())
    })
    
    fig2 = px.bar(
        age_range_df,
        x='Age Range',
        y='Count',
        title='Age Distribution of MPs 70 or Older',
        color_discrete_sequence=['#4CAF50'],
        text_auto=True
    )
    fig2.update_layout(
        xaxis_title='Age Range',
        yaxis_title='Number of Members'
    )
    fig2.write_html('senior_age_distribution.html')
    
    # Distribution by chamber
    chamber_counts = all_seniors['chamber'].value_counts()
    chamber_df = pd.DataFrame({'Chamber': chamber_counts.index, 'Count': chamber_counts.values})
    
    fig3 = px.bar(
        chamber_df,
        x='Chamber',
        y='Count',
        title='Distribution of Senior MPs by Chamber',
        color='Chamber',
        color_discrete_map={'Camera': '#FFA500', 'Senato': '#800080'},
        text_auto=True
    )
    fig3.update_layout(
        xaxis_title='Chamber',
        yaxis_title='Number of Members'
    )
    fig3.write_html('senior_chamber_distribution.html')
    
    # Comparison with overall Parliament composition
    total_camera = len(camera_members)
    total_senato = len(senato_members)
    total_parliament = total_camera + total_senato
    
    comparison_data = pd.DataFrame({
        'Chamber': ['Camera', 'Senato', 'Combined'],
        'Senior %': [
            (len(senior_camera) / total_camera * 100),
            (len(senior_senato) / total_senato * 100),
            (len(all_seniors) / total_parliament * 100)
        ]
    })
    
    fig4 = px.bar(
        comparison_data,
        x='Chamber',
        y='Senior %',
        title='Percentage of MPs 70 or Older by Chamber',
        color_discrete_sequence=['#8B4513'],
        text_auto='.1f'
    )
    fig4.update_layout(
        yaxis_title='Percentage of Members (%)',
        yaxis_range=[0, 50]  # Setting max to 50% for better visibility
    )
    fig4.write_html('senior_percentage.html')
    
    print("\nPlots have been saved as:")
    print("- senior_gender_distribution.html (Pie chart of gender distribution among senior MPs)")
    print("- senior_age_distribution.html (Bar chart of age distribution among senior MPs)")
    print("- senior_chamber_distribution.html (Bar chart of chamber distribution among senior MPs)")
    print("- senior_percentage.html (Bar chart showing percentage of senior MPs by chamber)")
else:
    print("No members found who are 70 years old or older.") 