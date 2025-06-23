from ChatBot import MeowBot
import sys

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("🚀 Starting MeowBot...")
    
    chatbot = MeowBot()
    chatbot.chat()

if __name__ == "__main__":
    main()