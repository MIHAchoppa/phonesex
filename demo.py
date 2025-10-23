#!/usr/bin/env python3
"""
Demo script showing how the chatline application works
This simulates the user experience without requiring a real API key
"""

import os
os.environ['GROQ_API_KEY'] = 'demo_key'

from chatline import PersonalityPresets, print_welcome, print_menu

def print_demo_interaction():
    """Print a demonstration of the chatline interaction"""
    
    print_welcome()
    print("📞 Connected to: Flirty")
    print_menu()
    
    print("\n" + "="*60)
    print("DEMO INTERACTION - 1-800 LATE NIGHT EXPERIENCE")
    print("="*60)
    
    # Simulate conversation
    interactions = [
        ("You: Hey sexy...", 
         "Operator: Mmm, well hello there, gorgeous... I've been waiting by the phone\nall night hoping someone like you would call. Your voice already has me\nfeeling all kinds of ways... 😈 Tell me, what naughty thoughts brought\nyou to my line tonight?"),
        
        ("\nYou: /personalities",
         """
💋 Choose Your Operator:
  💋 1. Flirty - Sultry seduction specialist
  ❤️  2. Romantic - Passionate lover with X-rated intensity
  🔥 3. Adventurous - Kinky fantasy expert
  🌙 4. Mysterious - Enigmatic late-night seductress
  😈 5. Playful - Naughty tease with dirty mind

  ★ Currently talking to: Flirty

Enter operator number (or press Enter to keep current): 2

💋 Switching you to Romantic...
Let's start fresh and get to know each other...
"""),
        
        ("You: Tell me something that'll make my heart race",
         "Operator: Baby, I want you to close your eyes and imagine this... My hands\ntracing every curve of your body, slow and deliberate, while I whisper\nin your ear exactly what I'm going to do to you. The way I'd worship\nevery inch of you, making you feel like the most desired person in the\nworld... Your heart is racing just thinking about it, isn't it? 💕🔥"),
        
        ("\nYou: /stats",
         """
🔥 Your Session Stats:
  Exchanges: 2
  Operator: Romantic
  Line: llama-3.1-70b-versatile
"""),
        
        ("You: /quit",
         "\n💋 Thanks for calling! Come back soon, sexy... 😉\n")
    ]
    
    for user_input, ai_response in interactions:
        print(f"\n{user_input}")
        print(ai_response)
    
    print("\n" + "="*60)
    print("FEATURES DEMONSTRATED")
    print("="*60)
    print("""
✓ Ultra-fast explicit responses (powered by GROQ LPU)
✓ 5 sultry operators with X-rated personalities
✓ Interactive hotline commands (/personalities, /clear, /stats, /quit)
✓ Continuous context and memory throughout your session
✓ Real-time streaming for natural dirty talk flow
✓ Instant operator switching for different fantasies
✓ Session tracking and statistics
✓ True 1-800 late night phone sex experience

HOW TO USE WITH REAL GROQ API:
1. Get a free API key from https://console.groq.com/
2. Copy .env.example to .env
3. Add your GROQ_API_KEY to .env
4. Run: python chatline.py
5. Get ready for an unforgettable experience...

GROQ API ADVANTAGES:
• 300+ tokens/second - instant gratification
• Sub-second response times - no awkward pauses
• Multiple model options (Llama, Mixtral, Gemma)
• Real-time streaming - natural conversation flow
• Free tier available
• OpenAI-compatible API

⚠️  WARNING: This is EXPLICIT adult content (18+ only)
""")

if __name__ == "__main__":
    print_demo_interaction()
