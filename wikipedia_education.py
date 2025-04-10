import wikipediaapi
import re
import pandas as pd
from typing import Set

def extract_education_from_text(text: str) -> Set[str]:
    # Common education-related terms in Italian and English
    education_terms = {
        'laurea', 'laureato', 'laureata', 'dottorato', 'dottore', 'dottorando', 'dottoranda',
        'master', 'specializzazione', 'specializzato', 'specializzata',
        'diploma', 'diplomato', 'diplomata', 'maturità', 'maturità classica', 'maturità scientifica',
        'degree', 'graduate', 'doctorate', 'doctor', 'phd', 'master', 'specialization', 'specialized',
        'diploma', 'high school', 'classical high school', 'scientific high school'
    }
    
    # Education patterns in Italian and English
    patterns = [
        # Complete degree statements
        r'(?i)(?:si è laureato|si è laureata|graduated|has graduated)\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)(?:\s+(?:presso|at|from)\s+[a-zA-ZÀ-ù\s]+)?\b',
        r'(?i)(?:laureato|laureata|graduated)\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)(?:\s+(?:presso|at|from)\s+[a-zA-ZÀ-ù\s]+)?\b',
        r'(?i)(?:dottorato|dottorata|doctorate)\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)(?:\s+(?:presso|at|from)\s+[a-zA-ZÀ-ù\s]+)?\b',
        r'(?i)(?:dottorato|dottorata|doctorate)\s+di\s+ricerca\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)(?:\s+(?:presso|at|from)\s+[a-zA-ZÀ-ù\s]+)?\b',
        r'(?i)(?:diploma|diplomato|diplomata|diploma)\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)(?:\s+(?:presso|at|from)\s+[a-zA-ZÀ-ù\s]+)?\b',
        r'(?i)(?:maturità|maturità classica|maturità scientifica|high school|classical high school|scientific high school)\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)(?:\s+(?:presso|at|from)\s+[a-zA-ZÀ-ù\s]+)?\b',
        
        # University patterns with field of study
        r'(?i)(?:presso|at|from)\s+([a-zA-ZÀ-ù\s]+?(?:University|Università|College|Istituto|Institute))\s+(?:in|in|as|with)\s+([a-zA-ZÀ-ù\s]+?)\b',
        
        # Field of study patterns
        r'(?i)(?:in|di|of)\s+([a-zA-ZÀ-ù\s]+?(?:studies|scienze|lettere|economia|giurisprudenza|medicina|ingegneria))\b'
    ]
    
    education = set()
    text = text.lower()
    
    # Extract education matches
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            # Get all capturing groups or the entire match if no groups
            if match.groups():
                # If we have multiple groups, combine them
                if len(match.groups()) > 1:
                    edu = ' '.join(group for group in match.groups() if group)
                else:
                    edu = match.group(1)
            else:
                edu = match.group(0)
                
            if edu is None:
                continue
                
            edu = edu.strip()
            
            # Skip if too short or contains numbers
            if len(edu) < 4 or any(c.isdigit() for c in edu):
                continue
                
            # Skip if it starts with common words that don't indicate education
            if edu.startswith(('il ', 'la ', 'lo ', 'the ', 'a ', 'an ', 'di ', 'del ', 'della ')):
                continue
                
            education.add(edu)
    
    return education

def search_wikipedia_education(name: str, surname: str) -> Set[str]:
    user_agent = 'ItalianParliamentResearch/1.0 (https://github.com/francescacollu/italian_parliament_representativeness)'
    wiki_it = wikipediaapi.Wikipedia(
        language='it',
        user_agent=user_agent
    )
    wiki_en = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent
    )
    
    all_education = set()
    
    # Try Italian Wikipedia
    page_it = wiki_it.page(f"{name} {surname}")
    if page_it.exists():
        print(f"Found Italian page: {page_it.fullurl}")
        print(f"Content snippet: {page_it.text[:200]}...")
        education_it = extract_education_from_text(page_it.text)
        print(f"Found education in Italian: {list(education_it)}")
        all_education.update(education_it)
    
    # Try English Wikipedia
    page_en = wiki_en.page(f"{name} {surname}")
    if page_en.exists():
        print(f"Found English page: {page_en.fullurl}")
        print(f"Content snippet: {page_en.text[:200]}...")
        education_en = extract_education_from_text(page_en.text)
        print(f"Found education in English: {list(education_en)}")
        all_education.update(education_en)
    
    return all_education

def main():
    # Read the dataset
    df = pd.read_csv('data/leg19_clean.csv')
    
    # Filter MPs with null titolo_studio
    null_education_df = df[df['titolo_studio'].isna()]
    print(f"Found {len(null_education_df)} MPs with missing educational qualifications")
    
    # Process each MP
    results = []
    for _, row in null_education_df.iterrows():
        name = row['nome']
        surname = row['cognome']
        print(f"\nProcessing {name} {surname}...")
        
        education = search_wikipedia_education(name, surname)
        if education:
            results.append({
                'nome': name,
                'cognome': surname,
                'titolo_studio': '; '.join(sorted(education))
            })
            print(f"Found education: {list(education)}")
        else:
            print("No education found")
    
    # Save results
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv('results/wikipedia_education.csv', index=False)
        print(f"\nSaved {len(results)} results to results/wikipedia_education.csv")

if __name__ == "__main__":
    main() 