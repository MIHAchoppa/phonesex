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
    print("Current personality: Flirty")
    print_menu()
    
    print("\n" + "="*60)
    print("DEMO INTERACTION")
    print("="*60)
    
    # Simulate conversation
    interactions = [
        ("You: Hey there!", 
         "AI: Well hello there, gorgeous! I've been waiting for someone interesting\nlike you to come along... 😉 What brings you to my corner of the world\ntonight?"),
        
        ("\nYou: /personalities",
         """
✨ Available Personalities:
  ★ 1. Flirty
    2. Romantic
    3. Adventurous
    4. Mysterious
    5. Playful

Enter personality number (or press Enter to cancel): 2

✨ Personality changed to: Romantic
Starting a fresh conversation...
"""),
        
        ("You: Tell me something sweet",
         "AI: You know, there's something truly special about this moment we're\nsharing. In a world that moves so fast, finding someone who wants to\nconnect on a deeper level is like discovering a hidden treasure. Your\npresence here makes my heart flutter with excitement... 💕"),
        
        ("\nYou: /stats",
         """
📊 Conversation Stats:
  Messages exchanged: 2
  Current personality: Romantic
  Model: llama-3.1-70b-versatile
"""),
        
        ("You: /quit",
         "\n👋 Thanks for chatting! Goodbye!\n")
    ]
    
    for user_input, ai_response in interactions:
        print(f"\n{user_input}")
        print(ai_response)
    
    print("\n" + "="*60)
    print("FEATURES DEMONSTRATED")
    print("="*60)
    print("""
✓ Ultra-fast streaming responses (powered by GROQ LPU)
✓ Multiple AI personalities (5 unique conversation styles)
✓ Interactive commands (/personalities, /clear, /stats, /quit)
✓ Conversation context maintenance
✓ Real-time response streaming
✓ Easy personality switching
✓ Conversation statistics tracking

HOW TO USE WITH REAL GROQ API:
1. Get a free API key from https://console.groq.com/
2. Copy .env.example to .env
3. Add your GROQ_API_KEY to .env
4. Run: python chatline.py
5. Start chatting!

GROQ API ADVANTAGES:
• 300+ tokens/second processing speed
• Sub-second response times
• Multiple model options (Llama, Mixtral, Gemma)
• Real-time streaming support
• Free tier available
• OpenAI-compatible API
""")

if __name__ == "__main__":
    print_demo_interaction()
