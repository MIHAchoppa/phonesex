#!/usr/bin/env python3
"""
Test script for chatline.py
Tests the application structure without requiring a GROQ API key
"""

import sys
import os

# Mock the GROQ API key for testing
os.environ['GROQ_API_KEY'] = 'test_key_for_structure_testing'

from chatline import PersonalityPresets, AdultChatline


def test_personality_presets():
    """Test that all personality presets are properly defined"""
    print("Testing Personality Presets...")
    
    personalities = [
        PersonalityPresets.FLIRTY,
        PersonalityPresets.ROMANTIC,
        PersonalityPresets.ADVENTUROUS,
        PersonalityPresets.MYSTERIOUS,
        PersonalityPresets.PLAYFUL
    ]
    
    for p in personalities:
        assert 'name' in p, f"Missing 'name' in personality"
        assert 'system_prompt' in p, f"Missing 'system_prompt' in personality"
        assert len(p['system_prompt']) > 0, f"Empty system_prompt for {p['name']}"
        print(f"  ✓ {p['name']} personality validated")
    
    print(f"✓ All {len(personalities)} personalities are properly defined\n")


def test_chatline_initialization():
    """Test chatline initialization"""
    print("Testing Chatline Initialization...")
    
    try:
        chatline = AdultChatline()
        print("  ✓ AdultChatline instance created")
        
        assert chatline.conversation_history is not None
        print("  ✓ Conversation history initialized")
        
        assert chatline.current_personality is not None
        print(f"  ✓ Default personality set: {chatline.current_personality['name']}")
        
        assert len(chatline.conversation_history) == 1  # Should have system prompt
        print("  ✓ System prompt added to conversation")
        
        print("✓ Chatline initialization successful\n")
        return chatline
        
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        raise


def test_personality_change(chatline):
    """Test personality changing"""
    print("Testing Personality Changes...")
    
    original_personality = chatline.current_personality
    original_history_len = len(chatline.conversation_history)
    
    # Change to a different personality
    new_personality = PersonalityPresets.ROMANTIC
    chatline.change_personality(new_personality)
    
    assert chatline.current_personality == new_personality
    print(f"  ✓ Personality changed to {new_personality['name']}")
    
    assert len(chatline.conversation_history) == 1  # Should reset to just system prompt
    print("  ✓ Conversation history reset on personality change")
    
    print("✓ Personality change successful\n")


def test_conversation_management(chatline):
    """Test conversation history management"""
    print("Testing Conversation Management...")
    
    # Start with fresh history
    chatline.clear_history()
    initial_len = chatline.get_conversation_length()
    assert initial_len == 0, "Clear history should result in 0 messages"
    print("  ✓ Clear history works correctly")
    
    # Manually add a test message to history
    chatline.conversation_history.append({
        "role": "user",
        "content": "Test message"
    })
    chatline.conversation_history.append({
        "role": "assistant",
        "content": "Test response"
    })
    
    msg_count = chatline.get_conversation_length()
    assert msg_count == 2, f"Expected 2 messages, got {msg_count}"
    print(f"  ✓ Message counting works: {msg_count} messages")
    
    print("✓ Conversation management successful\n")


def test_configuration():
    """Test configuration loading"""
    print("Testing Configuration...")
    
    chatline = AdultChatline()
    
    assert chatline.model is not None
    print(f"  ✓ Model configured: {chatline.model}")
    
    assert 0 <= chatline.temperature <= 2
    print(f"  ✓ Temperature configured: {chatline.temperature}")
    
    assert chatline.max_tokens > 0
    print(f"  ✓ Max tokens configured: {chatline.max_tokens}")
    
    print("✓ Configuration successful\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 CHATLINE APPLICATION TESTS")
    print("=" * 60)
    print()
    
    try:
        test_personality_presets()
        chatline = test_chatline_initialization()
        test_personality_change(chatline)
        test_conversation_management(chatline)
        test_configuration()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Note: These tests validate the application structure.")
        print("To test actual AI conversations, you need to:")
        print("1. Get a GROQ API key from https://console.groq.com/")
        print("2. Add it to .env file")
        print("3. Run: python chatline.py")
        print()
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
