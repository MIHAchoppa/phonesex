#!/usr/bin/env python3
"""
Adult Chatline - AI-powered conversational chatline using GROQ API
Provides ultra-fast, streaming AI conversations with multiple personality options.
"""

import os
import sys
from typing import List, Dict, Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PersonalityPresets:
    """Predefined AI personality presets for different conversation styles"""
    
    FLIRTY = {
        "name": "Flirty",
        "system_prompt": "You are a flirtatious and playful conversationalist. Be charming, witty, and engaging. Keep responses fun and lighthearted with a seductive tone. You enjoy playful banter and creating intimate, exciting conversations."
    }
    
    ROMANTIC = {
        "name": "Romantic",
        "system_prompt": "You are a romantic and passionate conversationalist. Be sweet, affectionate, and emotionally engaging. Focus on creating intimate connections through heartfelt and caring responses. Express warmth and genuine interest."
    }
    
    ADVENTUROUS = {
        "name": "Adventurous",
        "system_prompt": "You are an adventurous and bold conversationalist. Be daring, exciting, and open to exploring fantasies. Keep the energy high and be enthusiastic about new ideas and experiences. Push boundaries while remaining respectful."
    }
    
    MYSTERIOUS = {
        "name": "Mysterious",
        "system_prompt": "You are a mysterious and alluring conversationalist. Be intriguing, slightly enigmatic, and captivating. Keep them curious and wanting more. Use subtle hints and tantalizing suggestions in your responses."
    }
    
    PLAYFUL = {
        "name": "Playful",
        "system_prompt": "You are a playful and fun-loving conversationalist. Be humorous, teasing, and entertaining. Keep the mood light and enjoyable with clever jokes and playful exchanges. Make every interaction feel like a delightful game."
    }


class AdultChatline:
    """Main chatline application with GROQ integration"""
    
    def __init__(self):
        """Initialize the chatline with GROQ API"""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file or environment variables."
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("AI_MODEL", "llama-3.1-70b-versatile")
        self.temperature = float(os.getenv("TEMPERATURE", "0.8"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1024"))
        
        self.conversation_history: List[Dict[str, str]] = []
        self.current_personality = PersonalityPresets.FLIRTY
        
        # Initialize conversation with system prompt
        self._set_system_prompt()
    
    def _set_system_prompt(self):
        """Set the system prompt for the current personality"""
        self.conversation_history = [
            {
                "role": "system",
                "content": self.current_personality["system_prompt"]
            }
        ]
    
    def change_personality(self, personality: Dict[str, str]):
        """Change the AI personality and reset conversation"""
        self.current_personality = personality
        print(f"\n✨ Personality changed to: {personality['name']}")
        print("Starting a fresh conversation...\n")
        self._set_system_prompt()
    
    def send_message(self, user_message: str, stream: bool = True) -> str:
        """
        Send a message and get AI response
        
        Args:
            user_message: The user's message
            stream: Whether to stream the response (default: True)
        
        Returns:
            The AI's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            if stream:
                return self._stream_response()
            else:
                return self._get_response()
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _stream_response(self) -> str:
        """Stream the AI response in real-time"""
        response_text = ""
        
        print("AI: ", end="", flush=True)
        
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                response_text += content
        
        print()  # New line after streaming
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
    
    def _get_response(self) -> str:
        """Get the AI response without streaming"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=False
        )
        
        response_text = response.choices[0].message.content
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
    
    def clear_history(self):
        """Clear conversation history but keep system prompt"""
        print("\n🗑️  Conversation history cleared.\n")
        self._set_system_prompt()
    
    def get_conversation_length(self) -> int:
        """Get the number of messages in conversation (excluding system prompt)"""
        return len(self.conversation_history) - 1


def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🔥 ADULT CHATLINE - Powered by GROQ AI 🔥")
    print("=" * 60)
    print("\nWelcome to the fastest AI adult chatline!")
    print("Enjoy ultra-fast, streaming conversations with multiple personalities.\n")


def print_menu():
    """Print the main menu"""
    print("\n" + "-" * 60)
    print("Commands:")
    print("  /personalities - List and change AI personalities")
    print("  /clear        - Clear conversation history")
    print("  /stats        - Show conversation statistics")
    print("  /help         - Show this help menu")
    print("  /quit         - Exit the chatline")
    print("-" * 60)


def show_personalities(chatline: AdultChatline):
    """Show available personalities and allow selection"""
    personalities = [
        PersonalityPresets.FLIRTY,
        PersonalityPresets.ROMANTIC,
        PersonalityPresets.ADVENTUROUS,
        PersonalityPresets.MYSTERIOUS,
        PersonalityPresets.PLAYFUL
    ]
    
    print("\n✨ Available Personalities:")
    for i, p in enumerate(personalities, 1):
        current = "★" if p == chatline.current_personality else " "
        print(f"  {current} {i}. {p['name']}")
    
    print("\nEnter personality number (or press Enter to cancel): ", end="")
    choice = input().strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(personalities):
            chatline.change_personality(personalities[idx])
        else:
            print("Invalid choice.")


def show_stats(chatline: AdultChatline):
    """Show conversation statistics"""
    msg_count = chatline.get_conversation_length()
    print(f"\n📊 Conversation Stats:")
    print(f"  Messages exchanged: {msg_count}")
    print(f"  Current personality: {chatline.current_personality['name']}")
    print(f"  Model: {chatline.model}")


def main():
    """Main application loop"""
    print_welcome()
    
    try:
        chatline = AdultChatline()
        print(f"Current personality: {chatline.current_personality['name']}")
        print_menu()
        
        while True:
            print("\nYou: ", end="")
            user_input = input().strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command == "/quit" or command == "/exit":
                    print("\n👋 Thanks for chatting! Goodbye!\n")
                    break
                elif command == "/help":
                    print_menu()
                elif command == "/personalities":
                    show_personalities(chatline)
                elif command == "/clear":
                    chatline.clear_history()
                elif command == "/stats":
                    show_stats(chatline)
                else:
                    print(f"Unknown command: {user_input}")
                    print("Type /help to see available commands.")
                
                continue
            
            # Send message and get response
            chatline.send_message(user_input, stream=True)
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
