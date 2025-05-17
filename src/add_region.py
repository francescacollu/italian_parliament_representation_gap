import pandas as pd

def main():
    # Read the updated dataset
    df = pd.read_csv('data/leg19_clean_updated.csv')
    
    # Define mapping from provinces to regions
    province_to_region = {
        # Valle d'Aosta
        'Aosta': "Valle d'Aosta",
        
        # Piemonte
        'Alessandria': 'Piemonte',
        'Asti': 'Piemonte',
        'Biella': 'Piemonte',
        'Cuneo': 'Piemonte',
        'Novara': 'Piemonte',
        'Torino': 'Piemonte',
        'Verbano-Cusio-Ossola': 'Piemonte',
        'Verbano Cusio Ossola': 'Piemonte',
        'Verbania': 'Piemonte',
        'Vercelli': 'Piemonte',
        
        # Lombardia
        'Bergamo': 'Lombardia',
        'Brescia': 'Lombardia',
        'Como': 'Lombardia',
        'Cremona': 'Lombardia',
        'Lecco': 'Lombardia',
        'Lodi': 'Lombardia',
        'Monza e Brianza': 'Lombardia',
        'Monza E Della Brianza': 'Lombardia',
        'Monza': 'Lombardia',
        'Milano': 'Lombardia',
        'Mantova': 'Lombardia',
        'Pavia': 'Lombardia',
        'Sondrio': 'Lombardia',
        'Varese': 'Lombardia',
        
        # Trentino-Alto Adige
        'Bolzano': 'Trentino-Alto Adige',
        'Bolzano/Bozen': 'Trentino-Alto Adige',
        'Trento': 'Trentino-Alto Adige',
        
        # Veneto
        'Belluno': 'Veneto',
        'Padova': 'Veneto',
        'Rovigo': 'Veneto',
        'Treviso': 'Veneto',
        'Venezia': 'Veneto',
        'Vicenza': 'Veneto',
        'Verona': 'Veneto',
        
        # Friuli-Venezia Giulia
        'Gorizia': 'Friuli-Venezia Giulia',
        'Pordenone': 'Friuli-Venezia Giulia',
        'Trieste': 'Friuli-Venezia Giulia',
        'Udine': 'Friuli-Venezia Giulia',
        
        # Liguria
        'Genova': 'Liguria',
        'Imperia': 'Liguria',
        'La Spezia': 'Liguria',
        'Savona': 'Liguria',
        
        # Emilia-Romagna
        'Bologna': 'Emilia-Romagna',
        'Forlì-Cesena': 'Emilia-Romagna',
        "Forli'-Cesena": 'Emilia-Romagna',
        'Forlì': 'Emilia-Romagna',
        "Forli'": 'Emilia-Romagna',
        'Ferrara': 'Emilia-Romagna',
        'Modena': 'Emilia-Romagna',
        'Piacenza': 'Emilia-Romagna',
        'Parma': 'Emilia-Romagna',
        'Ravenna': 'Emilia-Romagna',
        'Reggio Emilia': 'Emilia-Romagna',
        "Reggio nell'Emilia": 'Emilia-Romagna',
        "Reggio Nell'Emilia": 'Emilia-Romagna',
        'Rimini': 'Emilia-Romagna',
        
        # Toscana
        'Arezzo': 'Toscana',
        'Firenze': 'Toscana',
        'Grosseto': 'Toscana',
        'Livorno': 'Toscana',
        'Lucca': 'Toscana',
        'Massa-Carrara': 'Toscana',
        'Massa Carrara': 'Toscana',
        'Massa': 'Toscana',
        'Pisa': 'Toscana',
        'Pistoia': 'Toscana',
        'Prato': 'Toscana',
        'Siena': 'Toscana',
        
        # Umbria
        'Perugia': 'Umbria',
        'Terni': 'Umbria',
        
        # Marche
        'Ancona': 'Marche',
        'Ascoli Piceno': 'Marche',
        'Fermo': 'Marche',
        'Macerata': 'Marche',
        'Pesaro e Urbino': 'Marche',
        'Pesaro E Urbino': 'Marche',
        'Pesaro': 'Marche',
        'Urbino': 'Marche',
        
        # Lazio
        'Frosinone': 'Lazio',
        'Latina': 'Lazio',
        'Rieti': 'Lazio',
        'Roma': 'Lazio',
        'Viterbo': 'Lazio',
        
        # Abruzzo
        "L'Aquila": 'Abruzzo',
        'Chieti': 'Abruzzo',
        'Pescara': 'Abruzzo',
        'Teramo': 'Abruzzo',
        
        # Molise
        'Campobasso': 'Molise',
        'Isernia': 'Molise',
        
        # Campania
        'Avellino': 'Campania',
        'Benevento': 'Campania',
        'Caserta': 'Campania',
        'Napoli': 'Campania',
        'Salerno': 'Campania',
        
        # Puglia
        'Bari': 'Puglia',
        'Brindisi': 'Puglia',
        'Barletta-Andria-Trani': 'Puglia',
        'Foggia': 'Puglia',
        'Lecce': 'Puglia',
        'Taranto': 'Puglia',
        
        # Basilicata
        'Matera': 'Basilicata',
        'Potenza': 'Basilicata',
        
        # Calabria
        'Cosenza': 'Calabria',
        'Catanzaro': 'Calabria',
        'Crotone': 'Calabria',
        'Reggio Calabria': 'Calabria',
        'Reggio di Calabria': 'Calabria',
        'Reggio Di Calabria': 'Calabria',
        'Vibo Valentia': 'Calabria',
        
        # Sicilia
        'Agrigento': 'Sicilia',
        'Caltanissetta': 'Sicilia',
        'Catania': 'Sicilia',
        'Enna': 'Sicilia',
        'Messina': 'Sicilia',
        'Palermo': 'Sicilia',
        'Ragusa': 'Sicilia',
        'Siracusa': 'Sicilia',
        'Trapani': 'Sicilia',
        
        # Sardegna
        'Cagliari': 'Sardegna',
        'Carbonia-Iglesias': 'Sardegna',
        'Nuoro': 'Sardegna',
        'Ogliastra': 'Sardegna',
        'Oristano': 'Sardegna',
        'Olbia-Tempio': 'Sardegna',
        'Sassari': 'Sardegna',
        'Sud Sardegna': 'Sardegna',
        'Medio Campidano': 'Sardegna',
        
        # Foreign countries - mark as 'Estero'
        'Svizzera': 'Estero',
        'Belgio': 'Estero',
        'Germania': 'Estero',
        'Argentina': 'Estero',
        "Costa D'Avorio": 'Estero',
        'Marocco': 'Estero'
    }
    
    # First, let's check the unique province values in the dataset
    unique_provinces = df['provincia_nascita'].dropna().unique()
    print(f"Found {len(unique_provinces)} unique province values")
    print(f"Sample of provinces: {sorted(unique_provinces)[:10]}")
    
    # Add regione_nascita column
    df['regione_nascita'] = df['provincia_nascita'].map(province_to_region)
    
    # Handle foreign-born MPs
    foreign_provinces = df[df['regione_nascita'].isna()]['provincia_nascita'].dropna().unique()
    print(f"\nFound {len(foreign_provinces)} provinces not mapped to Italian regions: {foreign_provinces}")
    
    # Mark these as 'Estero' (foreign)
    df.loc[df['regione_nascita'].isna() & df['provincia_nascita'].notna(), 'regione_nascita'] = 'Estero'
    
    # Count values
    print("\nRegion distribution:")
    print(df['regione_nascita'].value_counts())
    
    # Count null values
    null_regions = df['regione_nascita'].isna().sum()
    print(f"\nRecords with null regione_nascita: {null_regions}")
    
    # Save the updated dataset
    df.to_csv('data/leg19_clean_with_regions.csv', index=False)
    print(f"\nUpdated dataset saved to 'data/leg19_clean_with_regions.csv'")

if __name__ == "__main__":
    main() 