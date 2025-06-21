import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_file='chatbot_data.json', memory_file='conversation_memory.json'):
        self.data_file = data_file
        self.memory_file = memory_file
    
    def load_conversation_memory(self):
        """Load conversation history from JSON"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "conversations": [],
                "user_context": {},
                "session_count": 0
            }
    
    def save_conversation_memory(self, memory_data):
        """Save conversation history to JSON"""
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def add_message_to_memory(self, user_input, bot_response, user_context=None):
        """Add a message exchange to conversation memory"""
        memory = self.load_conversation_memory()
        
        message_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "bot_response": bot_response,
            "session_id": memory.get("session_count", 0)
        }
        
        memory["conversations"].append(message_entry)
        
        # Update user context if provided
        if user_context:
            memory["user_context"].update(user_context)
        
        # Keep only last 100 conversations to prevent file from getting too large
        if len(memory["conversations"]) > 100:
            memory["conversations"] = memory["conversations"][-100:]
        
        self.save_conversation_memory(memory)
        return memory
    
    def get_recent_conversations(self, limit=5):
        """Get recent conversation history"""
        memory = self.load_conversation_memory()
        return memory["conversations"][-limit:]
    
    def get_user_context(self):
        """Get stored user context (name, preferences, etc.)"""
        memory = self.load_conversation_memory()
        return memory.get("user_context", {})
    
    def start_new_session(self):
        """Start a new conversation session"""
        memory = self.load_conversation_memory()
        memory["session_count"] = memory.get("session_count", 0) + 1
        self.save_conversation_memory(memory)
        return memory["session_count"]
    
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default data if file doesn't exist
            default_data = self.get_default_data()
            self.save_data(default_data)
            return default_data
    
    def save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    #need to fix the sup and homie(name)
    def get_default_data(self): 
        return {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "yow", "howdy", "hola",
                             "good morning", "good afternoon", "good evening", "sup"],
                "responses": [
                    "Hello!",
                    "Hi there!",
                    "Hey!",
                    "What's Good?",
                    "Greetings!",
                    "Nice to meet you!",
                    "How can I help you today?",
                    "Greetings Huzz!",
                    "Sup?",
                    "What's good homie?"
                ]
            },
            "goodbye": {
                "patterns": ["bye", "goodbye", "see you", "farewell", "take care", "catch you later"],
                "responses": ["Goodbye!", "See you later!", "Take care!", "Bye!", "Have a great day!"]
            },
            "how_are_you": {
                "patterns": ["how are you", "how do you do", "how's it going", "what's up", "how are things"],
                "responses": ["I'm doing well, thank you!", "I'm great! How about you?", "All good here!", "I'm fine, thanks for asking!"]
            },
            "name": {
                "patterns": ["what is your name", "who are you", "what should I call you", "your name"],
                "responses": ["I'm MeowBot!", "You can call me MeowBot!", "I'm your friendly assistant, MeowBot!", "I'm just a cat bot here to help!"]
            },
            "help": {
                "patterns": ["help", "what can you do", "commands", "options"],
                "responses": ["I can chat with you! Try saying hello, asking how I am, or just have a conversation!", "I'm here to chat! Ask me anything!", "I can respond to greetings, questions about myself, and general conversation!"]
            },
            "thanks": {
                "patterns": ["thank you", "thanks", "appreciate it", "thx"],
                "responses": ["You're welcome!", "Happy to help!", "No problem!", "Anytime!", "Glad I could help!"]
            },
            "genz_slang": {
                "patterns": ["bet", "no cap", "cap", "slay", "slays", "rizz", "sus", "mid", "that's cap", "you're capping", "sus af", "lowkey sus", "big rizz", "no rizz", "mid af", "absolutely mid"],
                "responses": [
                    "Bet! I'm picking up what you're putting down! 💯",
                    "No cap, that's pretty cool! 🔥",
                    "Slay bestie! You're absolutely serving! ✨",
                    "Your energy is giving main character vibes! 💅",
                    "That's lowkey fire, not gonna lie! 🔥",
                    "Periodt! You understood the assignment! 💯",
                    "I see you with that energy! Keep slaying! ✨",
                    "Bestie, you're speaking facts right now! 📢",
                    "That's absolutely sending me! 😭",
                    "You're really out here being iconic! 👑",
                    "I'm here for this energy! Let's gooo! 🚀",
                    "This conversation is giving what it's supposed to give! ✨"
                ]
            },
            "genz_reactions": {
                "patterns": ["that's sus", "kinda sus", "sus behavior", "acting sus", "seems sus"],
                "responses": [
                    "Sus indeed! 👀 What's the tea?",
                    "I'm getting sus vibes too... spill! ☕",
                    "That's giving major sus energy ngl 🤔",
                    "Sus alert! 🚨 We need answers!"
                ]
            },
            "genz_mid": {
                "patterns": ["that's mid", "pretty mid", "kinda mid", "so mid", "mid energy"],
                "responses": [
                    "Oof, mid? That's rough buddy 😬",
                    "Mid is not the vibe we're going for! 📉",
                    "Mid hits different when you were expecting fire 💔",
                    "We don't settle for mid energy here! ✋"
                ]
            },
            "genz_cap": {
                "patterns": ["that's cap", "you're capping", "stop capping", "cap fr", "big cap"],
                "responses": [
                    "Cap? Me? Never! I only speak facts! 🧢",
                    "No cap detected here, bestie! 💯",
                    "I'm cap-free zone, trust! 🚫🧢",
                    "Zero cap in this household! Only truth! ✨"
                ]
            }
        }
    
    #not yet functional
    def add_intent(self, intent_name, patterns, responses):
        """Add a new intent to the chatbot data"""
        data = self.load_data()
        data[intent_name] = {
            'patterns': patterns,
            'responses': responses
        }
        self.save_data(data)
        return True