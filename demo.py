#!/usr/bin/env python3
"""
Demo script for the AI Adult Hotline
Demonstrates the functionality without requiring a real API key
"""
import os
from unittest.mock import Mock, patch


def demo_hotline():
    """Run a demo of the hotline with mocked responses"""
    print("\n" + "="*60)
    print("    AI Adult Hotline Demo")
    print("    (Using simulated AI responses)")
    print("="*60)
    print()
    
    # Mock responses for demo
    demo_conversation = [
        ("Hello, I'd like to talk.", "Hello! Thank you for calling. I'm here to chat with you. How are you doing today?"),
        ("I'm doing well, thanks!", "That's wonderful to hear! I'm glad you're doing well. What's on your mind today?"),
        ("Just wanted to have a nice conversation.", "I'd love that! Having meaningful conversations is what I'm here for. Tell me, what would you like to talk about?"),
        ("Tell me about yourself.", "I'm an AI assistant designed to provide warm, engaging conversation. I'm here to listen, chat, and make your time enjoyable. I'm always respectful and attentive to what you'd like to discuss."),
        ("quit", "Thank you for calling. Take care!")
    ]
    
    print("Demo Conversation:\n")
    for user_msg, ai_msg in demo_conversation:
        print(f"You: {user_msg}")
        if user_msg.lower() != "quit":
            print(f"AI: {ai_msg}\n")
        else:
            print(f"\n{ai_msg}\n")
    
    print("="*60)
    print("To use the real hotline:")
    print("1. Get an OpenAI API key from https://platform.openai.com/")
    print("2. Copy .env.example to .env")
    print("3. Add your API key to .env")
    print("4. Run: python hotline.py")
    print("="*60)
    print()


if __name__ == "__main__":
    demo_hotline()
