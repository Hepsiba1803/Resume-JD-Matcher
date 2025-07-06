import spacy, string
from keybert import KeyBERT
import csv


nlp = spacy.load('en_core_web_sm')
kw_model = KeyBERT('all-MiniLM-L6-v2')

def filter_missing_keywords(missing_keywords, text) -> set[str]:
     """ 
        Checks for noun phrases in the text that are present in missing keywords.

        Args:
            missing_keywords(set) : set of keywords not found in the skills set.
            text (str): The input text to extract noun phrases from.

            Returns:
             set[str]: A set of noun phrases that are present in the missing keywords.
     """
     
     doc = nlp(text)
     # Extract noun phrases from the text
     noun_phrases=set(chunk.text.lower().strip() for chunk in doc.noun_chunks)
     # Filter noun phrases that are in the missing keywords
     filtered_phrases = set(phrase for phrase in noun_phrases if phrase in missing_keywords)
     return filtered_phrases


    

def prompt_user_about_missing_skills(missing_keywords, csv_path):
    """
    Prompts the user to add missing keywords to the skills CSV file.

    Args:
        missing_keywords (set): Set of keywords not found in the skills set.
        csv_path (str): Path to the skills CSV file.
    """
    with open(csv_path, encoding="utf-8") as f:
        reader =csv.reader(f)
        next(reader)
        existing_skills=set(row[0].strip().lower() for row in reader if row and row[0].strip())
    if not missing_keywords:
        print("No missing keywords to add")
        return
    else:
        print("This is a simple functionality to improve our data set with new keywords")
        print(f"found {len(missing_keywords)} new keywords")
        for skill in missing_keywords:
            print(f"New Candidate skill/keyword: {skill}")
            if skill in existing_skills:
                        print(f"{skill} already exists in the dataset, skipping addition.")
                        continue
            else:
                response = input("please confirm this a valid skill/keyword: (yes/no):").strip().lower()
                if response == "yes":
                     category=input(f"Enter the category for {skill} (e.g., 'Programming Language', 'tool', 'technical skill', etc.)")
                     with open(csv_path, 'a', encoding="utf-8") as f:
                          writer = csv.writer(f)
                          writer.writerow([skill, category])
                          print(f"Added {skill} to the skills set under category {category}")
                          print("Thank you for helping us improve our skills set")
                else:
                     print(f"skipping {skill}, not a valid skill/keyword")
        
                    
csv_path = "backend/app/services/nlp/dataset.csv"

def load_skill_set(csv_path):
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        skills = set(row[0].strip().lower() for row in reader if row and row[0].strip())
    return skills

SKILL_SET = load_skill_set(csv_path)


def extract_relevant_skills_and_keywords(text, top_n=500) -> set[str]:
     """
    Extracts relevant skills and keywords from text using both a curated skills dictionary
    and KeyBERT for context-aware phrase extraction.

    Args:
        text (str): The input resume or JD text.
        top_n (int): Number of top KeyBERT phrases to extract.

    Returns:".csv
        Set[str]: Unique, relevant skills and key phrases.
    """ 

    # Extract skills from the curated skill set
     text = text.lower()
     
     # Use keybert to extract context-aware phrases
     keybert_phrases=set(kw for kw,_ in kw_model.extract_keywords(text, keyphrase_ngram_range=(1,3),stop_words='english', top_n=top_n))

     # keeping only those keybert phrases that are present in the skill set
     # Set of important short or non-alphabetic skills/keywords
     #ALWAYS_KEEP = {"ai", "ml", "r", "c", "go", "c++", "aws", ".net", "f#", "c#", "c#", "node.js", "js"}
     #filtered_keywords = {
       #  kw for kw in all_keywords
        #f len(kw) > 2
        #r " " in kw
       #or kw.lower() in ALWAYS_KEEP
     all_keywords = set()
     missing_keywords =set()
     for kw in keybert_phrases:
         if kw in SKILL_SET:
             all_keywords.add(kw.lower()) #Extracted keywords from keyBERT that are in the skill set
         else:
             missing_keywords.add(kw.lower())
     print("count:", len(all_keywords))
     #filtered_phrases = filter_missing_keywords(missing_keywords, text)
     # Prompt user to add missing keywords
     if False:
        prompt_user_about_missing_skills(missing_keywords, csv_path)
     return all_keywords

def load_skill_set_to_dict(csv_path) -> dict:
     """
        Loads the skills set from a CSV file into a dictionary.
        Args:
            csv_path(str) : Path to the CSV file containing skills and their categories.
        Returns:
            dict: A dictionary where keys are skills and values are their categories.
    """
     with open(csv_path, 'r', encoding="utf-8") as f_csv:
        reader = csv.DictReader(f_csv)
        dict_skill_set = {}
        # Read each row and populate the dictionary
        for row in reader:
            skill = row['skill'].strip().lower()
            category = row['category'].strip().lower()
            dict_skill_set[skill] = category
        return dict_skill_set


    