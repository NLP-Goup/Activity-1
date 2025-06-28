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
    
    def levenshtein_distance(self, s1, s2):
        """
        Calculate the Levenshtein distance between two strings.
        Returns the minimum number of single-character edits needed to transform s1 into s2.
        """
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        # store distances
        previous_row = list(range(len(s2) + 1))
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, and substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def levenshtein_similarity(self, s1, s2):
        """
        Convert Levenshtein distance to a similarity score between 0 and 1.
        Higher scores indicate more similar strings.
        """
        max_length = max(len(s1), len(s2))
        if max_length == 0:
            return 1.0  # Both strings are empty
        
        distance = self.levenshtein_distance(s1, s2)
        similarity = 1 - (distance / max_length)
        return similarity
    
    def calculate_similarity(self, user_input, pattern):
        """
        Calculate similarity between user input and pattern using multiple methods:
        1. Jaccard similarity (original method)
        2. Levenshtein similarity for exact phrase matching
        3. Token-level Levenshtein for individual words
        Returns the highest similarity score found.
        """
        # Preprocess both texts
        processed_input = self.preprocess(user_input)
        processed_pattern = self.preprocess(pattern)
        
        # Method 1: Original Jaccard similarity with stemming
        user_tokens = set(self.tokenize_and_stem(processed_input))
        pattern_tokens = set(self.tokenize_and_stem(processed_pattern))
        
        jaccard_similarity = 0
        if pattern_tokens:
            intersection = user_tokens.intersection(pattern_tokens)
            union = user_tokens.union(pattern_tokens)
            if union:
                jaccard_similarity = len(intersection) / len(union)
        
        # Method 2: Direct Levenshtein similarity on full phrases
        phrase_similarity = self.levenshtein_similarity(processed_input, processed_pattern)
        
        # Method 3: Token-level Levenshtein similarity
        # Find best matching tokens between input and pattern
        input_tokens = processed_input.split()
        pattern_tokens_list = processed_pattern.split()
        
        token_similarities = []
        if input_tokens and pattern_tokens_list:
            for input_token in input_tokens:
                best_token_match = max(
                    (self.levenshtein_similarity(input_token, pattern_token) 
                     for pattern_token in pattern_tokens_list),
                    default=0
                )
                token_similarities.append(best_token_match)
            
            # Average of best token matches
            avg_token_similarity = sum(token_similarities) / len(token_similarities)
        else:
            avg_token_similarity = 0
        
        # Return the highest similarity score from all methods
        return max(jaccard_similarity, phrase_similarity, avg_token_similarity)
    
    def find_closest_matches(self, user_input, patterns, threshold=0.3, top_n=3):
        """
        Find the closest matching patterns using Levenshtein distance.
        Returns a list of tuples: (pattern, similarity_score)
        Always returns float scores, never tuples.
        """
        matches = []
        
        for pattern in patterns:
            similarity = self.calculate_similarity(user_input, pattern)
            # Ensure similarity is always a float
            if isinstance(similarity, (int, float)) and similarity >= threshold:
                matches.append((pattern, float(similarity)))
        
        # Sort by similarity score (highest first) and return top N
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]
    
    def fuzzy_match(self, user_input, target_phrases, threshold=0.6):
        """
        Perform fuzzy matching using Levenshtein distance.
        Useful for handling typos and minor variations.
        Returns: (best_match_string, similarity_score) or (None, 0.0)
        """
        best_match = None
        best_score = 0.0
        
        processed_input = self.preprocess(user_input)
        
        for phrase in target_phrases:
            processed_phrase = self.preprocess(phrase)
            similarity = self.levenshtein_similarity(processed_input, processed_phrase)
            
            # Ensure similarity is a float
            similarity = float(similarity) if isinstance(similarity, (int, float)) else 0.0
            
            if similarity > best_score and similarity >= threshold:
                best_score = similarity
                best_match = phrase
        
        return (best_match, best_score) if best_match else (None, 0.0)