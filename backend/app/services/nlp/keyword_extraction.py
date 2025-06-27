import spacy
from spacy.lang.en.stop_words import STOP_WORDS

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "spaCy model 'en_core_web_sm' is not installed. "
        "Please run: python -m spacy download en_core_web_sm"
    )
def extract_keywords(text:str) -> set[str]:
    """
    Extract keywords from the given text using spaCy.

    Args:
        text (str): The input text from which to extract keywords.

    Returns:
        set: A set of keywords extracted from the text.
    """
    if not isinstance(text,str) or not text.strip():
        return set()
    doc = nlp(text)
    
    keywords = set()
    
    for token in doc:
         # Exclude stop words and punctuation, and consider only nouns and proper nouns
        if not token.is_stop and not token.is_punct and token.pos_ in{'NOUN', 'PROPN'}:
            # Normalize the keyword by converting it to lowercase and stripping whitespace
            keyword=token.lemma_.lower().strip() 
            if keyword:
                keywords.add(keyword)
    
    return keywords

