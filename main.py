<<<<<<< HEAD
from ChatBot import MeowBot
import sys

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("🚀 Starting MeowBot...")
    
    chatbot = MeowBot()
    chatbot.chat()

if __name__ == "__main__":
=======
from chatbot import MeowBot
import sys

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("🚀 Starting MeowBot...")
    
    chatbot = MeowBot()
    chatbot.chat()

if __name__ == "__main__":
>>>>>>> 1dd03d383ad3a53fd9f8dbdbb61a042fced9b622
    main()