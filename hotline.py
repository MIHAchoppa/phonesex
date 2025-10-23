#!/usr/bin/env python3
"""
AI Adult Hotline - An AI-powered conversational hotline
"""
import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class AdultHotline:
    """AI-powered adult hotline with conversational capabilities"""
    
    def __init__(self):
        """Initialize the hotline with OpenAI API"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it in .env file. "
                "See .env.example for reference."
            )
        
        self.client = OpenAI(api_key=api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = (
            "You are a friendly, engaging, and professional adult conversation "
            "partner on a hotline. Be conversational, respectful, and attentive "
            "to the caller's needs. Maintain appropriate boundaries while being "
            "warm and personable. Keep responses concise and natural."
        )
        
    def start_conversation(self):
        """Initialize a new conversation"""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        
    def get_response(self, user_message: str) -> str:
        """
        Get AI response for user message
        
        Args:
            user_message: The user's message
            
        Returns:
            AI-generated response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.8,
                max_tokens=200
            )
            
            # Extract assistant's reply
            assistant_message = response.choices[0].message.content
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run_interactive(self):
        """Run the hotline in interactive mode"""
        print("\n" + "="*60)
        print("    Welcome to the AI Adult Hotline")
        print("="*60)
        print("\nType your messages and press Enter to chat.")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        self.start_conversation()
        
        # Welcome message
        welcome = self.get_response("Hello, I'd like to talk.")
        print(f"AI: {welcome}\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\nAI: Thank you for calling. Take care!\n")
                    break
                
                # Get and display response
                response = self.get_response(user_input)
                print(f"\nAI: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nAI: Goodbye!\n")
                break
            except EOFError:
                break


def main():
    """Main entry point for the application"""
    try:
        hotline = AdultHotline()
        hotline.run_interactive()
    except ValueError as e:
        print(f"\nConfiguration Error: {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
