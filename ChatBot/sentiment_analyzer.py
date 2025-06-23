import re
import random

class GenZSentimentAnalyzer:
    def __init__(self):
        self.genz_sentiment = self.load_genz_sentiment()
    
    def load_genz_sentiment(self):
        """Load Gen Z sentiment dictionary"""
        return {
            # Positive Gen Z terms
            'positive': {
                'bet': 0.8, 'no cap': 0.9, 'slay': 0.95, 'slays': 0.95,
                'rizz': 0.7, 'fire': 0.9, 'vibes': 0.6, 'periodt': 0.8,
                'bestie': 0.7, 'iconic': 0.9, 'serving': 0.8, 'queen': 0.8,
                'king': 0.8, 'facts': 0.7, 'based': 0.7, 'bussin': 0.8,
                'slaps': 0.8, 'goated': 0.9, 'valid': 0.7, 'sends me': 0.8,
                'understood the assignment': 0.9, 'ate': 0.9, 'she ate': 0.9,
                'main character': 0.8, 'you ate that': 0.9, 'real one': 0.8,
                'hard launch': 0.7, 'it’s giving': 0.7, 'extra af': 0.8,
                'glow up': 0.8, 'living': 0.7, 'thriving': 0.7
            },
            # Negative Gen Z terms
            'negative': {
                'cap': -0.6, 'sus': -0.7, 'mid': -0.8, 'cringe': -0.9,
                'toxic': -0.9, 'salty': -0.6, 'ratio': -0.7, 'L': -0.8,
                'down bad': -0.7, 'cheugy': -0.6, 'pressed': -0.6,
                'rent free': -0.5, 'yikes': -0.7, 'ick': -0.8, 'flop': -0.8,
                'canceled': -0.9, 'dead': -0.8, 'NPC': -0.7, 'not it': -0.7,
                'dry af': -0.8, 'doing too much': -0.6, 'weird flex': -0.6,
                'clown': -0.7, 'broke behavior': -0.8
            },
            # Neutral Gen Z terms
            'neutral': {
                'lowkey': 0.0, 'highkey': 0.0, 'ngl': 0.0, 'fr': 0.0,
                'deadass': 0.0, 'bet that': 0.0, 'say less': 0.0,
                'it is what it is': 0.0, 'hits different': 0.0,
                'built different': 0.0, 'no shot': 0.0, 'periodt': 0.0,
                'not gonna lie': 0.0, 'real talk': 0.0, 'big mood': 0.0,
                'same energy': 0.0, 'vibe check': 0.0
            }
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of Gen Z terms in text"""
        text_lower = text.lower()
        sentiment_score = 0.0
        sentiment_words = []
        
        # Check all sentiment categories
        for sentiment_type, words in self.genz_sentiment.items():
            for word, score in words.items():
                if word in text_lower:
                    sentiment_score += score
                    sentiment_words.append({
                        'word': word,
                        'sentiment': sentiment_type,
                        'score': score
                    })
        
        # Determine overall sentiment
        if sentiment_score > 0.3:
            overall_sentiment = 'positive'
        elif sentiment_score < -0.3:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'score': sentiment_score,
            'overall': overall_sentiment,
            'words_found': sentiment_words,
            'intensity': abs(sentiment_score)
        }
    
    def get_sentiment_additions(self, sentiment_analysis):
        """Get additional response text based on sentiment"""
        sentiment = sentiment_analysis['overall']
        intensity = sentiment_analysis['intensity']
        
        if sentiment == 'positive':
            if intensity > 0.8:
                return "I'm picking up major positive vibes! 🔥✨"
            elif intensity > 0.5:
                return "Love the positive energy! ✨"
            else:
                return "Good vibes! 😊"
        elif sentiment == 'negative':
            if intensity > 0.8:
                return "Oof, that's giving rough energy 😬"
            elif intensity > 0.5:
                return "I sense some negative vibes 👀"
            else:
                return "Not the best vibes, but I get it 🤷‍♀️"
        else:
            return "I see you keeping it real! 💯"
    
    def generate_sentiment_response(self, sentiment_analysis):
        """Generate response based purely on sentiment analysis"""
        sentiment = sentiment_analysis['overall']
        words_found = [w['word'] for w in sentiment_analysis['words_found']]
        
        if sentiment == 'positive':
            positive_responses = [
                f"I love the positive energy with '{', '.join(words_found)}'! Keep slaying! ✨",
                f"Yes! The '{', '.join(words_found)}' energy is immaculate! 💯",
                f"You're really serving with that '{', '.join(words_found)}' vibe! 🔥",
                f"That positive '{', '.join(words_found)}' energy hits different! ✨"
            ]
            return random.choice(positive_responses)
        
        elif sentiment == 'negative':
            negative_responses = [
                f"I'm sensing some '{', '.join(words_found)}' vibes... what's the tea? ☕",
                f"Oop, the '{', '.join(words_found)}' energy is real... you okay bestie? 😬",
                f"That '{', '.join(words_found)}' mood is valid but let's turn it around! 💪",
                f"I feel the '{', '.join(words_found)}' sentiment... wanna talk about it? 👀"
            ]
            return random.choice(negative_responses)
        
        else:
            neutral_responses = [
                f"I see you with that '{', '.join(words_found)}' energy - keeping it real! 💯",
                f"The '{', '.join(words_found)}' vibe is noted! What's on your mind? 🤔",
                f"I'm picking up on the '{', '.join(words_found)}' - tell me more! 👀"
            ]
            return random.choice(neutral_responses)