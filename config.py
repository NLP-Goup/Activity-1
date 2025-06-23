CHATBOT_CONFIG = {
    'data_file': 'chatbot_data.json',
    'similarity_threshold': 0.3,
    'sentiment_threshold': {
        'positive': 0.3,
        'negative': -0.3
    },
    'max_response_length': 200,
    'enable_sentiment_analysis': True,
    'enable_logging': False,
    'log_file': 'chatbot.log'
}

# Emoji sets for different moods
EMOJI_SETS = {
    'positive': ['🔥', '✨', '💯', '😊', '👑', '🚀', '💪', '🎉'],
    'negative': ['😬', '👀', '☕', '🤔', '💔', '📉', '🚨', '😭'],
    'neutral': ['🤷‍♀️', '💭', '🗣️', '👂', '🎯', '📢', '💬', '🔮']
}
