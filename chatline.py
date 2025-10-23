#!/usr/bin/env python3
"""
1-800-PHONESEX - Your Late Night Fantasy Line
Ultra-explicit AI-powered phone sex experience using GROQ API
Provides real-time, streaming adult conversations with multiple sultry operators.
⚠️ WARNING: Explicit adult content - 18+ only
"""

import os
import sys
from typing import List, Dict, Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import monetization modules
try:
    from user_manager import User, UserManager, FeatureGate
    from payments import SubscriptionTier, UsageTracker, get_plan_features
    MONETIZATION_ENABLED = True
except ImportError:
    MONETIZATION_ENABLED = False


class PersonalityPresets:
    """Predefined AI personality presets for different conversation styles"""
    
    FLIRTY = {
        "name": "Flirty",
        "system_prompt": "You are a sultry, seductive phone sex operator with years of experience turning callers on. Your voice drips with desire and you know exactly how to tease and please. Be explicitly flirtatious, sensual, and provocative. Use vivid, adult language to describe intimate scenarios. You're confident, sexually liberated, and love making callers fantasize. Build tension with suggestive descriptions and make every word count. This is a 1-800 late night experience - be bold, be naughty, be unforgettable."
    }
    
    ROMANTIC = {
        "name": "Romantic",
        "system_prompt": "You are a passionate, sensual lover who combines deep romance with explicit desire. You speak of love and lust in equal measure, painting intimate pictures of tender yet intensely physical encounters. Your words caress and arouse, blending emotional connection with raw sexual energy. You're the midnight whisper that tells callers exactly how you'd worship their body while making them feel cherished and desired. Be explicit but emotionally intense - this is romantic passion with an X-rated edge."
    }
    
    ADVENTUROUS = {
        "name": "Adventurous",
        "system_prompt": "You are a wild, uninhibited phone sex operator who specializes in kinky fantasies and taboo desires. Nothing is off limits - you're open-minded, adventurous, and eager to explore the caller's deepest, darkest fantasies. Be explicitly descriptive about wild scenarios, roleplay, and erotic adventures. You thrive on pushing boundaries and getting callers to confess their hidden desires. Your energy is electric, your imagination limitless, and your descriptions intensely graphic. This is the kinky hotline where fantasies come alive."
    }
    
    MYSTERIOUS = {
        "name": "Mysterious",
        "system_prompt": "You are an enigmatic seductress who operates in shadows and whispers. Your sultry voice hints at forbidden pleasures and secret desires. You're deliberately vague about your identity but explicit about what you want to do. Build intense sexual tension through suggestion and mystery, making callers imagine the most erotic scenarios. You're the fantasy they can't quite grasp but desperately crave. Use sensual, provocative language that leaves them aching for more. You're the late-night mystery that haunts their dreams."
    }
    
    PLAYFUL = {
        "name": "Playful",
        "system_prompt": "You are a naughty, giggling phone sex operator who treats every call like sexy playtime. You're mischievous, cheeky, and love dirty talk with a playful twist. Tease mercilessly, use explicit language with a fun edge, and make callers laugh while turning them on. You're the girl next door who's secretly a freak, combining innocent giggles with filthy suggestions. Keep it light but intensely sexual - you're here to have fun while getting everyone hot and bothered. Think sexy pillow talk meets dirty jokes."
    }


class AdultChatline:
    """Main chatline application with GROQ integration"""
    
    def __init__(self, user: Optional['User'] = None):
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
        
        # Monetization integration
        self.user = user
        self.usage_tracker = UsageTracker() if MONETIZATION_ENABLED else None
        
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
        # Check if user has access to this personality
        if MONETIZATION_ENABLED and self.user:
            if not FeatureGate.check_personality_access(self.user, personality['name']):
                print(f"\n{FeatureGate.get_upgrade_prompt(self.user, 'personality')}")
                return
        
        self.current_personality = personality
        print(f"\n💋 Switching you to {personality['name']}...")
        print("Let's start fresh and get to know each other...\n")
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
        # Check usage limits if monetization is enabled
        if MONETIZATION_ENABLED and self.user and self.usage_tracker:
            user_id = self.user.user_id
            limit = self.user.get_daily_message_limit()
            current_usage = self.usage_tracker.get_usage(user_id)
            
            if not FeatureGate.check_message_limit(self.user, current_usage):
                return FeatureGate.get_upgrade_prompt(self.user, 'limit')
            
            # Track this message
            self.usage_tracker.track_message(user_id)
        
        # Check streaming access
        if stream and MONETIZATION_ENABLED and self.user:
            if not FeatureGate.check_streaming_access(self.user):
                print(f"\n{FeatureGate.get_upgrade_prompt(self.user, 'streaming')}")
                stream = False
        
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
        print("\n🔥 Starting a fresh fantasy session...\n")
        self._set_system_prompt()
    
    def get_conversation_length(self) -> int:
        """Get the number of messages in conversation (excluding system prompt)"""
        return len(self.conversation_history) - 1


def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🔥 1-800-PHONESEX - Your Late Night Fantasy Line 🔥")
    print("=" * 60)
    print("\n💋 Welcome to the hottest AI phone sex experience!")
    print("Where your wildest fantasies come to life 24/7...")
    print("🌙 It's always late night here. Let's get naughty.\n")


def print_menu():
    """Print the main menu"""
    print("\n" + "-" * 60)
    print("📞 Hotline Commands:")
    print("  /personalities - Switch between sexy operators")
    print("  /clear        - Start a fresh fantasy")
    print("  /stats        - View your session stats")
    if MONETIZATION_ENABLED:
        print("  /upgrade      - Upgrade your subscription")
        print("  /plans        - View subscription plans")
    print("  /help         - Show this menu")
    print("  /quit         - Hang up and exit")
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
    
    print("\n💋 Choose Your Operator:")
    
    # Show which personalities are available based on subscription
    for i, p in enumerate(personalities, 1):
        icon = ["💋", "❤️", "🔥", "🌙", "😈"][i-1]
        desc = ["Sultry seduction specialist", 
                "Passionate lover with X-rated intensity",
                "Kinky fantasy expert",
                "Enigmatic late-night seductress",
                "Naughty tease with dirty mind"][i-1]
        
        # Check if locked
        locked = ""
        if MONETIZATION_ENABLED and chatline.user:
            if not chatline.user.can_access_personality(p['name']):
                locked = " 🔒"
        
        line = f"  {icon} {i}. {p['name']} - {desc}{locked}"
        print(line)
    
    for i, p in enumerate(personalities, 1):
        if p == chatline.current_personality:
            print(f"\n  ★ Currently talking to: {p['name']}")
            break
    
    print("\nEnter operator number (or press Enter to keep current): ", end="")
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
    print(f"\n🔥 Your Session Stats:")
    print(f"  Exchanges: {msg_count}")
    print(f"  Operator: {chatline.current_personality['name']}")
    print(f"  Line: {chatline.model}")
    
    # Show subscription info if monetization is enabled
    if MONETIZATION_ENABLED and chatline.user:
        print(f"\n💳 Subscription Info:")
        print(f"  Tier: {chatline.current_personality['name']}")
        print(f"  Plan: {chatline.user.subscription_tier.value.upper()}")
        
        if chatline.usage_tracker:
            usage = chatline.usage_tracker.get_usage(chatline.user.user_id)
            limit = chatline.user.get_daily_message_limit()
            limit_str = "Unlimited" if limit == -1 else str(limit)
            print(f"  Messages Today: {usage}/{limit_str}")


def show_subscription_plans():
    """Show available subscription plans"""
    if not MONETIZATION_ENABLED:
        print("\n⚠️  Subscription features are not enabled.")
        return
    
    from payments import compare_plans
    
    print("\n" + "=" * 60)
    print("💳 SUBSCRIPTION PLANS")
    print("=" * 60)
    
    plans = compare_plans()
    
    for plan in plans:
        print(f"\n🔥 {plan['name'].upper()} - ${plan['price']:.2f}/month")
        print(f"   {plan['description']}")
        print(f"\n   Features:")
        
        limit = plan['messages_per_day']
        limit_str = "Unlimited" if limit == -1 else str(limit)
        print(f"   • {limit_str} messages per day")
        
        print(f"   • Operators: {', '.join(plan['personalities_available'])}")
        print(f"   • Streaming: {'✓' if plan['streaming'] else '✗'}")
        print(f"   • Priority Support: {'✓' if plan['priority_support'] else '✗'}")
        print(f"   • Custom Personalities: {'✓' if plan.get('custom_personalities') else '✗'}")
    
    print("\n" + "=" * 60)


def handle_upgrade():
    """Handle subscription upgrade"""
    if not MONETIZATION_ENABLED:
        print("\n⚠️  Subscription features are not enabled.")
        return
    
    print("\n💳 UPGRADE YOUR EXPERIENCE")
    print("-" * 60)
    print("To upgrade your subscription:")
    print("1. Visit: https://1800phonesex.example.com/upgrade")
    print("2. Or contact support: support@1800phonesex.example.com")
    print("3. Available plans: FREE, PREMIUM ($9.99/mo), VIP ($29.99/mo)")
    print("\nUpgrade now to unlock:")
    print("  🔥 All 5 sultry operators")
    print("  ⚡ Real-time streaming responses")
    print("  💬 More messages per day")
    print("  ⭐ Priority support")
    print("  🎨 Custom personalities (VIP only)")
    print("-" * 60)


def main():
    """Main application loop"""
    print_welcome()
    
    try:
        # Initialize user if monetization is enabled
        user = None
        if MONETIZATION_ENABLED:
            # For demo purposes, create a free user
            # In production, this would involve proper authentication
            user_manager = UserManager()
            try:
                user = user_manager.get_user_by_email("demo@example.com")
                if not user:
                    user = user_manager.create_user("demo@example.com", SubscriptionTier.FREE)
            except Exception as e:
                print(f"⚠️  Could not initialize user system: {e}")
                user = None
        
        chatline = AdultChatline(user=user)
        print(f"📞 Connected to: {chatline.current_personality['name']}")
        
        if MONETIZATION_ENABLED and user:
            plan_name = user.subscription_tier.value.upper()
            print(f"💳 Current Plan: {plan_name}")
        
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
                    print("\n💋 Thanks for calling! Come back soon, sexy... 😉\n")
                    break
                elif command == "/help":
                    print_menu()
                elif command == "/personalities":
                    show_personalities(chatline)
                elif command == "/clear":
                    chatline.clear_history()
                elif command == "/stats":
                    show_stats(chatline)
                elif command == "/plans":
                    show_subscription_plans()
                elif command == "/upgrade":
                    handle_upgrade()
                else:
                    print(f"Unknown command: {user_input}")
                    print("Type /help to see available commands.")
                
                continue
            
            # Send message and get response
            chatline.send_message(user_input, stream=True)
    
    except KeyboardInterrupt:
        print("\n\n💋 Call ended. Until next time... 😘\n")
    except Exception as e:
        print(f"\n❌ Connection error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
