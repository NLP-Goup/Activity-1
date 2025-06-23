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
     
     
    #  still fixing when it come to name  
    def extract_user_info(self, user_input):
        """Extract user information from input (name, preferences, etc.)"""
        user_context = {}
        
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                user_context["name"] = match.group(1).capitalize()
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
        """Enhance response with context from previous conversations"""
        user_context = self.data_manager.get_user_context()
        recent_conversations = self.data_manager.get_recent_conversations(3)
        
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
            
            #need to fix when askingf name
            # If user asks about their name and we don't have it stored
            if "my name" in user_input.lower() and "name" not in user_context:
                # Check if they mentioned their name in recent conversations
                for conv in recent_conversations:
                    if "my name is" in conv["user_input"].lower():
                        name_match = re.search(r"my name is (\w+)", conv["user_input"].lower())
                        if name_match:
                            return f"You told me your name is {name_match.group(1).capitalize()}!"
        
        return base_response
    
    def get_response(self, user_input):
        """Generate response with conversation memory"""
        if not user_input.strip():
            return "I didn't catch that. Could you say something?"
        
        # Extract any user information from current input
        user_context_update = self.extract_user_info(user_input)
        
        # Analyze Gen Z sentiment
        sentiment_analysis = self.sentiment_analyzer.analyze_sentiment(user_input)
        
        # Find best matching intent (existing logic)
        best_match = None
        best_score = 0
        threshold = 0.3
        
        for intent, intent_data in self.data.items():
            patterns = intent_data.get('patterns', [])
            for pattern in patterns:
                similarity = self.text_processor.calculate_similarity(user_input, pattern)
                if similarity > best_score and similarity >= threshold:
                    best_score = similarity
                    best_match = intent
        
        # create base response
        if best_match:
            responses = self.data[best_match].get('responses', [])
            base_response = random.choice(responses) if responses else "I understand, but I'm not sure how to respond."
        elif sentiment_analysis['words_found']:
            base_response = self.sentiment_analyzer.generate_sentiment_response(sentiment_analysis)
        else:
            base_response = random.choice([
                "I'm sorry, I don't understand that.",
                "Could you rephrase that?",
                "That's interesting! Tell me more.",
                "I'm still learning. Can you try asking something else?"
            ])
        
        # response with conversation context
        final_response = self.get_context_aware_response(user_input, base_response)
        
        # Add sentiment additions if applicable
        if sentiment_analysis['words_found'] and best_match:
            sentiment_additions = self.sentiment_analyzer.get_sentiment_additions(sentiment_analysis)
            final_response += f" {sentiment_additions}"
        
        # Save this conversation to memory
        self.data_manager.add_message_to_memory(
            user_input=user_input,
            bot_response=final_response,
            user_context=user_context_update if user_context_update else None
        )
        
        return final_response
    
    def show_memory_stats(self):
        """Show conversation memory statistics"""
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
    
    def chat(self):
        print("🐱 MeowBot: Hello! I'm your friendly catbot! Type 'exit' to end.")
        print("🐱 MeowBot: Commands: 'add intent' | 'memory stats' | 'clear memory'")
        
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