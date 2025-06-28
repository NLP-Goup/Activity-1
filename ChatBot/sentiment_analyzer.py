import re
import random
from typing import Dict, List, Tuple

class GenZSentimentAnalyzer:
    def __init__(self):
        self.sentiment_words = {
            'positive': {
                # Standard positive
                'love': 0.8, 'like': 0.6, 'enjoy': 0.7, 'amazing': 0.9, 'great': 0.8,
                'awesome': 0.9, 'nice': 0.6, 'good': 0.6, 'wonderful': 0.8, 'perfect': 0.9,
                'happy': 0.8, 'excited': 0.8, 'fantastic': 0.9, 'excellent': 0.9,
                
                # Gen Z positive
                'slay': 0.9, 'fire': 0.9, 'bet': 0.7, 'vibes': 0.6, 'iconic': 0.8,
                'bussin': 0.8, 'goated': 0.9, 'valid': 0.7, 'based': 0.7, 'periodt': 0.8,
                'no cap': 0.8, 'slaps': 0.8, 'hits different': 0.8, 'goes hard': 0.9
            },
            'negative': {
                # Standard negative
                'hate': -0.9, 'dislike': -0.7, 'bad': -0.7, 'terrible': -0.9, 'awful': -0.9,
                'annoying': -0.7, 'boring': -0.6, 'sad': -0.7, 'angry': -0.8, 'upset': -0.7,
                'frustrated': -0.7, 'disappointed': -0.6,
                
                # Gen Z negative
                'mid': -0.7, 'cringe': -0.8, 'toxic': -0.9, 'sus': -0.6, 'cap': -0.6,
                'trash': -0.8, 'flop': -0.8, 'L': -0.7, 'ratio': -0.7, 'yikes': -0.7
            }
        }
        
        self.emoji_sentiment = {
            '😍': 0.9, '😊': 0.7, '😂': 0.8, '🥰': 0.8, '😁': 0.7, '🤩': 0.9,
            '🔥': 0.8, '✨': 0.7, '💯': 0.8, '👑': 0.8, '💕': 0.7, '❤️': 0.8,
            '😭': -0.3, '😢': -0.7, '😠': -0.8, '😡': -0.9, '🤮': -0.9, '💔': -0.8,
            '😬': -0.5, '🙄': -0.4, '😤': -0.6, '🤡': -0.7, '💀': 0.2  # 💀 can be positive in Gen Z context
        }
        
        self.intensity_modifiers = {
            'very': 1.5, 'super': 1.7, 'really': 1.4, 'so': 1.3, 'extremely': 1.8,
            'totally': 1.5, 'absolutely': 1.6, 'hella': 1.6, 'mad': 1.4, 'crazy': 1.3,
            'kinda': 0.7, 'sorta': 0.6, 'pretty': 1.2, 'lowkey': 0.8
        }
        
        self.negation_words = {'not', 'never', 'no', "don't", "isn't", "won't", "can't", "shouldn't"}
    
    def preprocess_text(self, text: str) -> str:
        """Handle multi-word Gen Z phrases"""
        text = re.sub(r'\bno cap\b', 'NOCAP_POSITIVE', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhits different\b', 'HITSDIFFERENT_POSITIVE', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgoes hard\b', 'GOESHARD_POSITIVE', text, flags=re.IGNORECASE)
        return text
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment with chatbot-friendly output"""
        processed_text = self.preprocess_text(text)
        words = processed_text.lower().split()
        
        sentiment_score = 0.0
        found_words = []
        
        # Check emojis
        emoji_score = sum(self.emoji_sentiment.get(char, 0) for char in text)
        sentiment_score += emoji_score
        
        # Analyze words with context
        for i, word in enumerate(words):
            # Clean word
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            # Check for sentiment
            word_score = None
            if clean_word in self.sentiment_words['positive']:
                word_score = self.sentiment_words['positive'][clean_word]
            elif clean_word in self.sentiment_words['negative']:
                word_score = self.sentiment_words['negative'][clean_word]
            elif clean_word == 'nocap_positive':
                word_score = 0.8
            elif clean_word in ['hitsdifferent_positive', 'goeshard_positive']:
                word_score = 0.8
            
            if word_score is not None:
                # Check for intensity modifiers
                modifier = 1.0
                if i > 0 and words[i-1] in self.intensity_modifiers:
                    modifier = self.intensity_modifiers[words[i-1]]
                
                # Check for negation
                negated = False
                if i > 0 and any(words[j] in self.negation_words for j in range(max(0, i-2), i)):
                    negated = True
                    word_score *= -0.7
                
                final_score = word_score * modifier
                sentiment_score += final_score
                
                found_words.append({
                    'word': clean_word,
                    'score': final_score,
                    'negated': negated,
                    'modifier': modifier
                })
        
        # Determine overall sentiment
        if sentiment_score > 0.4:
            overall = 'positive'
        elif sentiment_score < -0.4:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'score': round(sentiment_score, 2),
            'overall': overall,
            'intensity': round(abs(sentiment_score), 2),
            'words_found': found_words,
            'emoji_score': round(emoji_score, 2),
            'confidence': min(1.0, abs(sentiment_score) / 2.0)
        }
    
    def get_sentiment_response_modifier(self, sentiment_result: Dict) -> str:
        """Get response modifier based on sentiment - perfect for your chatbot"""
        overall = sentiment_result['overall']
        intensity = sentiment_result['intensity']
        confidence = sentiment_result['confidence']
        
        if confidence < 0.3:
            return ""  # Low confidence, don't modify
        
        if overall == 'positive':
            if intensity > 1.0:
                return random.choice([
                    "Your energy is absolutely contagious! ✨",
                    "Love the main character energy! 🔥",
                    "You're absolutely slaying right now! 👑"
                ])
            else:
                return random.choice([
                    "Love the good vibes! 😊",
                    "That positive energy hits different! ✨",
                    "You're bringing the vibes! 💯"
                ])
        
        elif overall == 'negative':
            if intensity > 1.0:
                return random.choice([
                    "That sounds really tough... I'm here if you need to chat 💙",
                    "Sending you good vibes, that sounds rough 🤗",
                    "Hope things get better for you soon! 💜"
                ])
            else:
                return random.choice([
                    "I hear you... 🤗",
                    "That doesn't sound great, want to talk about it?",
                    "Hope I can help brighten your day a bit! 😊"
                ])
        
        return ""
    
    def generate_sentiment_response(self, sentiment_result: Dict) -> str:
        """Generate contextual response """
        overall = sentiment_result['overall']
        words = [w['word'] for w in sentiment_result['words_found']]
        
        if overall == 'positive' and words:
            return random.choice([
                f"I love that '{words[0]}' energy! Tell me more! ✨",
                f"Yes! That '{words[0]}' vibe is everything! 🔥",
                f"You're bringing that '{words[0]}' energy and I'm here for it! 💯"
            ])
        
        elif overall == 'negative' and words:
            return random.choice([
                f"I'm picking up on some '{words[0]}' vibes... want to talk about it? 🤗",
                f"That '{words[0]}' feeling is valid... I'm here to listen! 💜",
                f"Sorry you're dealing with '{words[0]}' stuff... how can I help? 😊"
            ])
        
        else:
            return random.choice([
                "What's on your mind? I'm all ears! 👂",
                "Tell me more about what you're thinking! 💭",
                "I'm here for whatever you want to chat about! 😊"
            ])
    
    def should_use_sentiment_response(self, sentiment_result: Dict, has_intent_match: bool) -> bool:
        """Helper to decide when to use sentiment-based responses"""
        return (
            not has_intent_match and 
            sentiment_result['confidence'] > 0.4 and 
            len(sentiment_result['words_found']) > 0
        )