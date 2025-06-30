import random
import re
from .sentiment_analyzer import GenZSentimentAnalyzer
from .text_processor import TextProcessor 
from .data_manager import DataManager

class MeowBot:
    def __init__(self, data_file=r'ChatBot\data\chatbot_data.json'):
        self.data_manager = DataManager(data_file)
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = GenZSentimentAnalyzer()
        self.data = self.data_manager.load_data()
        self.session_id = self.data_manager.start_new_session()
     
    def extract_user_info(self, user_input):
        user_context = {}
        
        wellbeing_phrases = [
            "doing great", "doin great", "doing good", "doin good",
            "doing fine", "doin fine", "doing well", "doin well",
            "i'm good", "im good", "i'm fine", "im fine",
            "i'm well", "im well", "i'm okay", "im okay",
            "i'm feeling well", "im feeling well", "feeling well", 
            "feeling good", "feeling great", "feeling fine"    
        ]
        
        non_name_words = {
            'also', 'just', 'really', 'very', 'quite', 'actually', 
            'doing', 'feeling', 'good', 'great', 'well', 'fine',
            'sad', 'happy', 'angry', 'excited', 'tired', 'bored',
            'confused', 'stressed', 'worried', 'nervous', 'scared',
            'disappointed', 'frustrated', 'annoyed', 'upset', 'mad',
            'glad', 'pleased', 'thrilled', 'delighted', 'content'
        }
        
        lower_input = user_input.lower()
        if any(phrase in lower_input for phrase in wellbeing_phrases):
            return user_context  
        
        name_patterns = [
            r"^(?:hi|hello|hey),?\s*(?:my name is|i'?m|i am)\s+(\w+)",
            r"(?:my name is|i'?m|i am)\s+(\w+)(?:$|[\.,!?])",
            r"call me\s+(\w+)"
        ]
        
        
        for pattern in name_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                possible_name = match.group(1).lower()
                if (len(possible_name) > 2 and 
                    possible_name not in non_name_words and
                    possible_name.isalpha()):
                    user_context["name"] = possible_name.capitalize()
                    break
        
        
        # preferences
        if "i like" in user_input.lower():
            preference = user_input.lower().split("i like")[1].strip()
            if "likes" not in user_context:
                user_context["likes"] = []
            user_context["likes"].append(preference)
        
        if "i hate" in user_input.lower() or "i don't like" in user_input.lower():
            dislike = user_input.lower().replace("i hate", "").replace("i don't like", "").strip()
            if "dislikes" not in user_context:
                user_context["dislikes"] = []
            user_context["dislikes"].append(dislike)
        
        return user_context
    
    def get_context_aware_response(self, user_input, base_response):
        user_context = self.data_manager.get_user_context()
        recent_conversations = self.data_manager.get_recent_conversations(5)

        if any(phrase in user_input.lower() for phrase in ["what is my name", "what's my name", "who am i", "do you know my name", "tell me my name", "my name"]):
            if "name" in user_context:
                from random import choice
                bot_data = self.data_manager.load_data()
                user_name_intent = bot_data.get("user_name", {})
                responses = user_name_intent.get("responses", [])
                if responses:
                    return choice(responses).replace("{name}", user_context["name"])
                else:
                    return f"Your name is {user_context['name']}!"
            else:
                return "Hmm, I don't think you told me your name yet!"
                
        if "name" in user_context:
            name = user_context["name"]
            if "hello" in user_input.lower() or "hi" in user_input.lower():
                return f"Hey {name}! {base_response}"
            elif any(word in user_input.lower() for word in ["how are you", "what's up", "how's it going", "what's good"]):
                return f"I'm doing great, {name}! {base_response}"
        
        # Reference previous topics if relevant
        if recent_conversations:
            last_conversation = recent_conversations[-1]
            
            # If user asks "what did I just say" or similar
            if any(phrase in user_input.lower() for phrase in ["what did i say", "what was i talking about", "before", "earlier"]):
                return f"You were saying: '{last_conversation['user_input']}'"
        
        return base_response
    
    def find_best_intent_match(self, user_input, threshold=0.3):
        """Find the best matching intent using enhanced Levenshtein distance."""
        best_matches = []
        
        # Collect all patterns with their intents and similarity scores
        for intent, intent_data in self.data.items():
            patterns = intent_data.get('patterns', [])
            
            # Use the enhanced similarity calculation
            pattern_matches = self.text_processor.find_closest_matches(
                user_input, patterns, threshold=threshold, top_n=1
            )
            
            if pattern_matches:
                best_pattern, best_score = pattern_matches[0]
                best_matches.append((intent, best_pattern, best_score))
        
        if best_matches:
            best_matches.sort(key=lambda x: x[2], reverse=True)
            return best_matches[0]  # (intent, pattern, score)
        
        return (None, None, 0.0) 
    
    def handle_typos_and_variations(self, user_input):
        """Handle common typos"""
        common_phrases = [
            "hello", "goodbye", "thank you", "how are you", "what's up",
            "help me", "what can you do", "who are you", "what is your name"
        ]
        
        # it tries to find the closest match using fuzzy matching
        closest_match, similarity = self.text_processor.fuzzy_match(
            user_input, common_phrases, threshold=0.6
        )
        
        if closest_match and similarity > 0.7:
            return closest_match
        
        return user_input  # Return original if no good match found
    
    def is_name_introduction(self, user_input):
        """
        Check if the input is specifically a name introduction
        """
        # Emotion words that should NOT be treated as names
        emotion_words = {
            'sad', 'happy', 'angry', 'excited', 'tired', 'bored',
            'confused', 'stressed', 'worried', 'nervous', 'scared',
            'disappointed', 'frustrated', 'annoyed', 'upset', 'mad',
            'glad', 'pleased', 'thrilled', 'delighted', 'content',
            'fine', 'good', 'great', 'well', 'okay', 'alright'
        }
        
        name_patterns = [
            r"(?:hi|hello|hey),?\s*(?:my name is|i'?m|i am)\s+(\w+)",
            r"(?:my name is)\s+(\w+)",
            r"(?:call me)\s+(\w+)",
            r"^(?:i'?m|i am)\s+(\w+)(?:\s+and|$|[\.,!?])",  
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                possible_name = match.group(1).lower()
                # Check if it's not an emotion word and is a valid name
                if (len(possible_name) > 1 and 
                    possible_name not in emotion_words and
                    possible_name.isalpha() and
                    possible_name != 'not'):  # Exclude common words like 'not'
                    return possible_name.capitalize()
        
        return None
    
    def get_response(self, user_input):
        if not user_input.strip():
            return "I didn't catch that. Could you say something?"
        
        # Handle potential typos first
        corrected_input = self.handle_typos_and_variations(user_input)
        
        # Extract any user information from current input
        user_context_update = self.extract_user_info(user_input)

        # Check for name introduction using the improved method
        introduced_name = self.is_name_introduction(user_input)
        if introduced_name:
            self.data_manager.add_message_to_memory(
                user_input, 
                f"Hey there, {introduced_name}!", 
                user_context={"name": introduced_name}
            )
            return f"Hey there, {introduced_name}!"

        # Analyze Gen Z sentiment
        sentiment_analysis = self.sentiment_analyzer.analyze_sentiment(user_input)
        
        # Find best matching intent using enhanced similarity with Levenshtein distance
        match_result = self.find_best_intent_match(corrected_input, threshold=0.2)
        
        if match_result[0] is not None:  # Check if we found a match
            best_intent, best_pattern, best_score = match_result
        else:
            best_intent, best_pattern, best_score = None, None, 0.0
        
        # Debug information (you can remove this in production)
        if best_intent and best_score > 0:
            print(f"🔍 Matched Word: '{best_pattern}' in '{best_intent}' with score {best_score:.3f}")
        
        if best_intent and best_score >= 0.2:
            responses = self.data[best_intent].get('responses', [])
            base_response = random.choice(responses) if responses else "I understand, but I'm not sure how to respond."
        elif self.sentiment_analyzer.should_use_sentiment_response(sentiment_analysis, False):
             base_response = self.sentiment_analyzer.generate_sentiment_response(sentiment_analysis)
        else:
            # Suggest similar commands if no match found
            all_patterns = []
            for intent_data in self.data.values():
                all_patterns.extend(intent_data.get('patterns', []))
            
            closest_patterns = self.text_processor.find_closest_matches(
                user_input, all_patterns, threshold=0.15, top_n=2
            )
            
            if closest_patterns:
                suggestions = [pattern for pattern, _ in closest_patterns]
                base_response = f"I'm not sure about that. Did you mean something like: {' or '.join(suggestions)}?"
            else:
                base_response = random.choice([
                    "I'm sorry, I don't understand that.",
                    "Could you rephrase that?",
                    "That's interesting! Tell me more.",
                    "I'm still learning. Can you try asking something else?"
                ])

        final_response = self.get_context_aware_response(user_input, base_response)
        
        if sentiment_analysis['confidence'] > 0.5:
            sentiment_modifier = self.sentiment_analyzer.get_sentiment_response_modifier(sentiment_analysis)
            if sentiment_modifier:
                final_response += f" {sentiment_modifier}"
        
        # Save this conversation to memory
        self.data_manager.add_message_to_memory(
            user_input=user_input,
            bot_response=final_response,
            user_context=user_context_update if user_context_update else None
        )
        
        return final_response
    
    def show_memory_stats(self):
        memory = self.data_manager.load_conversation_memory()
        user_context = memory.get("user_context", {})
        conversation_count = len(memory.get("conversations", []))
        
        print(f"\n📊 Memory Stats:")
        print(f"   Total conversations: {conversation_count}")
        print(f"   Current session: {self.session_id}")
        
        if user_context:
            print(f"   What I know about you:")
            for key, value in user_context.items():
                print(f"     {key}: {value}")
        else:
            print(f"   I don't know much about you yet!")
    
    def interactive_add_intent(self):
        print("🐱 MeowBot: Interactive intent addition feature coming soon!")
        pass
    
    def chat(self):
        print("🐱 MeowBot: Hello! I'm your friendly catbot with enhanced understanding! Type 'exit' to end.")
        print("🐱 MeowBot: Commands: 'add intent' | 'memory stats' | 'clear memory'")
        print("🐱 MeowBot: I can now better understand typos and variations in your messages!")
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🐱 MeowBot: Goodbye! I'll remember our chat!")
                    break
                
                if user_input.lower() == 'memory stats':
                    self.show_memory_stats()
                    continue
                
                if user_input.lower() == 'clear memory':
                    self.data_manager.save_conversation_memory({
                        "conversations": [],
                        "user_context": {},
                        "session_count": 0
                    })
                    print("🐱 MeowBot: Memory cleared! Starting fresh.")
                    continue
                
                if user_input.lower() == 'add intent':
                    self.interactive_add_intent()
                    continue
                
                if not user_input:
                    continue
                
                response = self.get_response(user_input)
                print(f"🐱 MeowBot: {response}")
                
            except KeyboardInterrupt:
                print("\n🐱 MeowBot: Goodbye! I'll remember our chat!")
                break
            except Exception as e:
                print(f"🐱 MeowBot: Sorry, I encountered an error: {e}")