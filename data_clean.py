import pandas as pd
import re

def extract_id(url):
    return url.split('/')[-1]

def clean_capitalized_data(data):
    if pd.isna(data):
        return None 
    return data.title()

def clean_genere(genere):
    if genere == 'male':
        return 'M'
    elif genere == 'female':
        return 'F'
    else:
        return genere

def wrangle_data_nascita(data_nascita):
    if pd.isna(data_nascita):
        return None
    
    # Convert integer to string if needed
    if isinstance(data_nascita, int):
        data_nascita = str(data_nascita)
    
    if isinstance(data_nascita, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', data_nascita):
        return data_nascita
    
    try:
        if isinstance(data_nascita, str):
            if len(data_nascita) == 8:
                return f"{data_nascita[:4]}-{data_nascita[4:6]}-{data_nascita[6:8]}"
        return data_nascita
    except:
        return data_nascita
    
def extract_titolo_professione(descrizione):
    """
    Extract titolo di studio and professione from the descrizione field.
    If there's a semicolon, split into titolo and professione.
    If there's no semicolon, assume the entire string is titolo di studio.
    """
    if pd.isna(descrizione):
        return None, None
    
    parts = descrizione.split(';', 1)
    
    if len(parts) == 2:
        titolo = parts[0].strip()
        professione = parts[1].strip()
    else:
        titolo = parts[0].strip()
        professione = None
    
    return titolo, professione

def create_tipo_mandato(row):
    if pd.isna(row['tipoMandato']):
        return 'elettivo'
    else:
        return row['tipoMandato']

def wrangle_provincia_nascita(nato):
    if pd.isna(nato):
        return None
    
    if isinstance(nato, str):
        return nato.split(',')[1].strip().title()
    return nato


camera_df = pd.read_csv('data/Camera_Leg19.csv')
senato_df = pd.read_csv('data/Senato_Leg19.csv')

# Extract IDs from URLs
camera_df['id'] = camera_df['persona'].apply(extract_id)
senato_df['id'] = senato_df['senatore'].apply(extract_id)

# Rename columns to match between datasets
camera_df = camera_df.rename(columns={
    'persona': 'url',
    'nome': 'nome',
    'cognome': 'cognome',
    'genere': 'genere',
    'dataNascita': 'data_nascita',
    'luogoNascita': 'citta_nascita',
    'descrizione': 'professione',
})

senato_df = senato_df.rename(columns={
    'senatore': 'url',
    'nome': 'nome',
    'cognome': 'cognome',
    'genere': 'genere',
    'dataNascita': 'data_nascita',
    'cittaNascita': 'citta_nascita',
    'provinciaNascita': 'provincia_nascita',
    'Professione': 'professione'
})

camera_df['id'] = camera_df['url'].apply(extract_id)
senato_df['id'] = senato_df['url'].apply(extract_id)

camera_df['nome'] = camera_df['nome'].apply(clean_capitalized_data)
camera_df['cognome'] = camera_df['cognome'].apply(clean_capitalized_data)
camera_df['citta_nascita'] = camera_df['citta_nascita'].apply(clean_capitalized_data)
camera_df['provincia_nascita'] = camera_df['nato'].apply(wrangle_provincia_nascita)

camera_df['titolo_studio'], camera_df['professione'] = zip(*camera_df['professione'].apply(extract_titolo_professione))
camera_df['titolo_studio'] = camera_df['titolo_studio'].apply(clean_capitalized_data)
camera_df['professione'] = camera_df['professione'].apply(clean_capitalized_data)

camera_df['genere'] = camera_df['genere'].apply(clean_genere)
senato_df['genere'] = senato_df['genere'].apply(clean_genere)

camera_df['data_nascita'] = camera_df['data_nascita'].apply(wrangle_data_nascita)
senato_df['data_nascita'] = senato_df['data_nascita'].apply(wrangle_data_nascita)

camera_df['tipo_mandato'] = 'elettivo'
senato_df['tipo_mandato'] = senato_df.apply(create_tipo_mandato, axis=1)

df = pd.concat([camera_df, senato_df])

df = df[['id', 'nome', 'cognome', 'genere', 'data_nascita', 'citta_nascita', 'provincia_nascita', 'titolo_studio', 'professione', 'tipo_mandato']]

df = df.drop_duplicates()
# Group by all columns except 'professione' and aggregate 'professione' into a list
df = df.groupby(['id', 'nome', 'cognome', 'genere', 'data_nascita', 'citta_nascita', 'provincia_nascita', 'titolo_studio', 'tipo_mandato'], as_index=False, dropna=False).agg({
    'professione': list  # Simply convert to list without filtering None values
})

df.to_csv('data/leg19_clean.csv', index=False)