# File: tests/test_nlp_processor.py

import unittest
from unittest.mock import patch

# Adjust import according to your project structure
try:
    from app.services.nlp.keyword_extraction import extract_keywords
    from app.services.nlp.match_score import match_score 
    from app.services.nlp.generate_match_report import match_report
except ImportError:
    # If you run tests from a different location, you may need to adjust the import path
    # For example, if running from the project root with PYTHONPATH set:
   from backend.app.services.nlp.keyword_extraction import extract_keywords
   from backend.app.services.nlp.match_score import match_score 
   from backend.app.services.nlp.generate_match_report import match_report
class TestNLPFunctions(unittest.TestCase):

    def test_extract_keywords_basic(self):
        text = "Python developer with experience in FastAPI and AWS."
        keywords = extract_keywords(text)
        self.assertIn('python', keywords)
        self.assertIn('developer', keywords)
        self.assertIn('fastapi', keywords)
        self.assertIn('aws', keywords)

    def test_extract_keywords_empty(self):
        self.assertEqual(extract_keywords(''), set())
        self.assertEqual(extract_keywords('   '), set())
        self.assertEqual(extract_keywords(None), set())

    def test_compute_similarity_identical(self):
        text1 = "python fastapi aws"
        text2 = "python fastapi aws"
        score= match_score(text1, text2)
        self.assertAlmostEqual(score, 1.0, places=2)

    def test_compute_similarity_different(self):
        text1 = "python fastapi"
        text2 = "java spring"
        score = match_score(text1, text2)
        self.assertAlmostEqual(score, 0.0, places=2)

    def test_calculate_match_score(self):
        resume_text = "Experienced Python developer with AWS and Docker."
        jd_text = "Looking for a Python developer with experience in AWS and Kubernetes."
        result = match_report(resume_text, jd_text)
        self.assertIn('match_score', result)
        self.assertIn('resume_keywords', result)
        self.assertIn('jd_keywords', result)
        self.assertIsInstance(result['match_score'], float)
        self.assertIsInstance(result['resume_keywords'], list)
        self.assertIsInstance(result['jd_keywords'], list)

if __name__ == '__main__':
    unittest.main()
