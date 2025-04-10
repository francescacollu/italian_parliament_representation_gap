import pandas as pd
import wikipediaapi
import re
from typing import List, Optional, Dict

def extract_jobs_from_text(content: str, lang: str) -> List[str]:
    """Extract jobs and roles from text content."""
    jobs = []
    
    # Common job/role patterns
    patterns = {
        'it': [
            # Professional roles
            r"(?:è stato|è stata|è|era)(?:\s+un[ao]?)?\s+([^,.]+?(?:ore|ista|ante|iere|ico|ogo|ere)[^,.]*)",
            # Work experience
            r"ha (?:lavorato|operato) (?:come|presso|nel|alla|per)\s+([^,.]+?(?:(?:dal|fino al|nel) \d{4})?)",
            # Specific roles
            r"(?:direttore|presidente|amministratore|consigliere|segretario|docente|professore|dirigente)\s+(?:di|del|della|presso|all[ao])\s+([^,.]+?(?:(?:dal|fino al|nel) \d{4})?)",
            # Education
            r"(?:laureato|laureata) in\s+([^,.]+?(?:presso [^,.]+)?)",
            # Teaching
            r"(?:docente|professore) (?:di|in)\s+([^,.]+?(?:presso [^,.]+)?)",
            # Employment
            r"(?:impiegato|impiegata|dipendente) (?:presso|di|del|della)\s+([^,.]+)"
        ],
        'en': [
            # Professional roles
            r"(?:was|is|has been)(?: an?)?\s+([^,.]+?(?:er|ist|ant|or|ian)[^,.]*?(?:(?:from|until|in) \d{4})?)",
            # Work experience
            r"worked (?:as|at|for|in)\s+([^,.]+?(?:(?:from|until|in) \d{4})?)",
            # Specific roles
            r"(?:director|president|administrator|counselor|secretary|teacher|professor|manager) (?:of|at|in)\s+([^,.]+?(?:(?:from|until|in) \d{4})?)",
            # Education
            r"graduated (?:in|with)\s+([^,.]+?(?:from [^,.]+)?)",
            # Teaching
            r"(?:teaches|taught)\s+([^,.]+?(?:at [^,.]+)?)",
            # Employment
            r"employed (?:at|by)\s+([^,.]+)"
        ]
    }
    
    # Words to filter out
    filter_words = {
        'it': [
            'politico', 'politica', 'italiano', 'italiana', 'deputato', 'deputata', 
            'parlamentare', 'membro', 'eletto', 'eletta', 'nominato', 'nominata',
            'consiglio', 'movimento', 'partito', 'camera', 'senato'
        ],
        'en': [
            'politician', 'italian', 'member', 'deputy', 'parliamentary',
            'elected', 'appointed', 'council', 'movement', 'party', 'chamber',
            'senate', 'born', 'welcomed'
        ]
    }
    
    for pattern in patterns[lang]:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            job = match.group(1).strip().lower()
            # Filter out common political roles, dates, and short matches
            if (len(job) > 3 and 
                not any(x in job for x in filter_words[lang]) and
                not any(x in job.lower() for x in ['un', 'una', 'il', 'la', 'the', 'a', 'an']) and
                not re.match(r'^\d+$', job) and  # Filter out just numbers
                not re.match(r'^[^a-zA-Z]+$', job)):  # Must contain at least one letter
                jobs.append(job)
    
    return list(set(jobs))

def search_wikipedia_profession(name: str, surname: str) -> Optional[List[str]]:
    """
    Search Wikipedia for a person's previous jobs and roles.
    Returns a list of jobs if found, None otherwise.
    """
    try:
        # Initialize Wikipedia API for both languages
        wiki_en = wikipediaapi.Wikipedia(
            language='en',
            user_agent='ItalianParliamentResearch/1.0 (https://github.com/yourusername/italian_parliament_representativeness)'
        )
        wiki_it = wikipediaapi.Wikipedia(
            language='it',
            user_agent='ItalianParliamentResearch/1.0 (https://github.com/yourusername/italian_parliament_representativeness)'
        )
        
        all_jobs = []
        # Try both languages
        for wiki, lang in [(wiki_it, 'it'), (wiki_en, 'en')]:  # Try Italian first
            # Try different search variations
            search_variations = [
                f"{name}_{surname}",  # Wikipedia style
                f"{name} {surname}",   # Simple name
            ]
            
            for query in search_variations:
                print(f"Trying {query} in {lang}...")
                page = wiki.page(query)
                
                if not page.exists():
                    continue
                
                # Print the page URL
                print(f"Found page: {page.fullurl}")
                print(f"Page title: {page.title}")
                
                # Get the page content
                content = page.text.lower()
                
                # Extract jobs from the content
                jobs = extract_jobs_from_text(content, lang)
                if jobs:
                    print(f"Found jobs in {lang}: {jobs}")
                    all_jobs.extend(jobs)
                    
        return list(set(all_jobs)) if all_jobs else None
        
    except Exception as e:
        print(f"Error processing {name} {surname}: {str(e)}")
        return None

def main():
    # Read the CSV file
    df = pd.read_csv("results/missing_profession_mp.csv")
    
    # Create a new column for Wikipedia professions
    df['wikipedia_profession'] = None
    
    # Process each MP
    for idx, row in df.iterrows():
        print(f"\nProcessing {row['nome']} {row['cognome']}...")
        jobs = search_wikipedia_profession(row['nome'], row['cognome'])
        if jobs:
            df.at[idx, 'wikipedia_profession'] = str(jobs)
    
    # Save results
    df.to_csv("results/wikipedia_professions.csv", index=False)
    print("\nDone! Results saved to results/wikipedia_professions.csv")

if __name__ == "__main__":
    main() 