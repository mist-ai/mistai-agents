import spacy
from gliner_spacy.pipeline import GlinerSpacy

class KeywordExtractor:
    def __init__(self, labels=None):
        """
        Initializes the KeywordExtractor with specified labels.
        :param labels: List of entity labels to extract.
        """
        if labels is None:
            labels = ['Company', 'StockExchange', 'Person', 'Sector']
        
        self.nlp = spacy.blank('en')
        self.nlp.add_pipe('gliner_spacy', config={"labels": labels})
    
    def extract(self, text):
        """
        Extracts keywords from the given text.
        :param text: str
        :return: dict of keywords with their entity types
        """
        doc = self.nlp(text)
        return {ent.text: ent.label_ for ent in doc.ents}

# Example usage:
extractor = KeywordExtractor()
# keywords = extractor.extract("HNB is listed on CSE.")

# print(keywords)