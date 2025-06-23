import re

class TextProcessor:
    def __init__(self):
        pass
    
    def preprocess(self, text):
        """Clean and preprocess the input text"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def simple_stem(self, word):
        """Simple stemming function (removes common suffixes)"""
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 's']
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)]
        return word
    
    def tokenize_and_stem(self, text):
        """Tokenize text and apply simple stemming"""
        # Simple tokenization by splitting on whitespace
        tokens = text.split()
        
        # Apply simple stemming
        stemmed_tokens = [self.simple_stem(token) for token in tokens]
        
        return stemmed_tokens
    
    def calculate_similarity(self, user_input, pattern):
        """Calculate similarity between user input and pattern"""
        user_tokens = set(self.tokenize_and_stem(self.preprocess(user_input)))
        pattern_tokens = set(self.tokenize_and_stem(self.preprocess(pattern)))
        
        if not pattern_tokens:
            return 0
        
        # Calculate Jaccard similarity
        intersection = user_tokens.intersection(pattern_tokens)
        union = user_tokens.union(pattern_tokens)
        
        if not union:
            return 0
        
        return len(intersection) / len(union)