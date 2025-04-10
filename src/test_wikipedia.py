import wikipediaapi
import re
import pandas as pd
from typing import List, Set

def extract_jobs_from_text(text: str) -> Set[str]:
    # Common political terms to exclude
    political_terms = {
        'deputato', 'senatore', 'ministro', 'presidente', 'sindaco', 'consigliere',
        'assessore', 'parlamentare', 'europarlamentare', 'mep', 'onorevole',
        'deputy', 'senator', 'minister', 'president', 'mayor', 'councillor',
        'alderman', 'parliamentarian', 'mep', 'honorable', 'politico', 'politician',
        'leader', 'capo', 'chief', 'head', 'prime minister', 'premier'
    }
    
    # List of known professions in Italian and English
    professions = {
        'giornalista', 'journalist',
        'avvocato', 'lawyer',
        'medico', 'doctor',
        'insegnante', 'teacher',
        'professore', 'professor',
        'imprenditore', 'entrepreneur',
        'commercialista', 'accountant',
        'architetto', 'architect',
        'ingegnere', 'engineer',
        'scrittore', 'writer',
        'autore', 'author',
        'ricercatore', 'researcher',
        'consulente', 'consultant',
        'dirigente', 'manager',
        'artista', 'artist',
        'musicista', 'musician',
        'attore', 'actor',
        'regista', 'director',
        'produttore', 'producer'
    }
    
    # Job title patterns in Italian and English
    patterns = [
        # Direct profession mentions
        r'(?i)\b(?:' + '|'.join(professions) + r')\b(?:\s+(?:professionista|professional|specializzato|specialized))?\b',
        
        # Role patterns
        r'(?i)(?:è|è stata|ha lavorato come|worked as|was|has been)\s+(?:un[ao]\s+)?([a-zA-ZÀ-ù]{4,}(?:ista|ore|ante|iere|ico|ogo|er|or|ian|ist))\b',
        
        # Education/qualification based roles
        r'(?i)(?:laureata?|graduated)\s+(?:in|as)\s+([a-zA-ZÀ-ù]{4,}(?:ista|ore|ante|iere|ico|ogo|er|or|ian|ist))\b'
    ]
    
    jobs = set()
    text = text.lower()
    
    # Extract job matches
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            # Get all capturing groups or the entire match if no groups
            job = match.group(1) if match.groups() else match.group(0)
            job = job.strip()
            
            # Skip if too short or contains numbers
            if len(job) < 4 or any(c.isdigit() for c in job):
                continue
                
            # Skip if it's a political term
            if any(term in job.lower() for term in political_terms):
                continue
                
            # Skip if it starts with common words that don't indicate professions
            if job.startswith(('il ', 'la ', 'lo ', 'the ', 'a ', 'an ', 'di ', 'del ', 'della ')):
                continue
                
            # Skip if it's a verb or common non-profession word
            common_verbs = {'stata', 'stato', 'been', 'was', 'is', 'sono', 'era', 'were', 'are'}
            if job in common_verbs:
                continue
                
            jobs.add(job)
    
    return jobs

def search_wikipedia_profession(name: str, surname: str) -> Set[str]:
    user_agent = 'ItalianParliamentResearch/1.0 (https://github.com/francescacollu/italian_parliament_representativeness)'
    wiki_it = wikipediaapi.Wikipedia(
        language='it',
        user_agent=user_agent
    )
    wiki_en = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent
    )
    
    all_jobs = set()
    
    # Try Italian Wikipedia
    page_it = wiki_it.page(f"{name} {surname}")
    if page_it.exists():
        print(f"Found Italian page: {page_it.fullurl}")
        print(f"Content snippet: {page_it.text[:200]}...")
        jobs_it = extract_jobs_from_text(page_it.text)
        print(f"Found jobs in Italian: {list(jobs_it)}")
        all_jobs.update(jobs_it)
    
    # Try English Wikipedia
    page_en = wiki_en.page(f"{name} {surname}")
    if page_en.exists():
        print(f"Found English page: {page_en.fullurl}")
        print(f"Content snippet: {page_en.text[:200]}...")
        jobs_en = extract_jobs_from_text(page_en.text)
        print(f"Found jobs in English: {list(jobs_en)}")
        all_jobs.update(jobs_en)
    
    return all_jobs

def main():
    # Read the missing professions file
    df = pd.read_csv('results/missing_profession_mp.csv')
    
    # Process each MP
    results = []
    for _, row in df.iterrows():
        name = row['nome']
        surname = row['cognome']
        print(f"\nProcessing {name} {surname}...")
        
        jobs = search_wikipedia_profession(name, surname)
        if jobs:
            results.append({
                'nome': name,
                'cognome': surname,
                'professione': '; '.join(sorted(jobs))
            })
            print(f"Found professions: {list(jobs)}")
        else:
            print("No professions found")
    
    # Save results
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv('results/wikipedia_professions.csv', index=False)
        print(f"\nSaved {len(results)} results to results/wikipedia_professions.csv")

if __name__ == "__main__":
    main() 