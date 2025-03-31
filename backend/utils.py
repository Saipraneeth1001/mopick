import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

def normalize_prompt(prompt: str) -> str:
    prompt = prompt.lower()
    prompt = prompt.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(prompt)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)
