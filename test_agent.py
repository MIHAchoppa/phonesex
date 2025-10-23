#!/usr/bin/env python3
"""
Test script for agent.py
Tests the voice agent structure without requiring full LiveKit connection.
"""

import os
import sys

# Mock the required API keys for testing
os.environ['GROQ_API_KEY'] = 'test_key_for_structure_testing'
os.environ['ELEVEN_API_KEY'] = 'test_key_for_structure_testing'

from livekit import agents
from livekit.plugins import groq, elevenlabs
import agent


def test_agent_imports():
    """Test that all required imports work correctly"""
    print("Testing agent.py imports...")
    
    assert hasattr(agents, 'voice'), "LiveKit voice module not found"
    assert hasattr(groq, 'STT'), "Groq STT not found"
    assert hasattr(groq, 'LLM'), "Groq LLM not found"
    assert hasattr(elevenlabs, 'TTS'), "ElevenLabs TTS not found"
    
    print("  ✓ All imports are available\n")


def test_agent_structure():
    """Test that agent.py has the required structure"""
    print("Testing agent.py structure...")
    
    assert hasattr(agent, 'prewarm'), "prewarm function not found"
    assert hasattr(agent, 'entrypoint'), "entrypoint function not found"
    assert hasattr(agent, 'logger'), "logger not configured"
    
    assert callable(agent.prewarm), "prewarm is not callable"
    
    # Check if entrypoint is an async function
    import inspect
    assert inspect.iscoroutinefunction(agent.entrypoint), "entrypoint is not an async function"
    
    print("  ✓ Agent structure is valid")
    print(f"  ✓ prewarm function exists: {callable(agent.prewarm)}")
    print(f"  ✓ entrypoint is async: {inspect.iscoroutinefunction(agent.entrypoint)}")
    print(f"  ✓ logger configured: {hasattr(agent, 'logger')}\n")


def test_agent_instantiation():
    """Test that the voice agent can be instantiated"""
    print("Testing voice agent instantiation...")
    
    instructions = (
        "You are a helpful and enthusiastic travel agent assistant. "
        "Your name is Journey."
    )
    
    try:
        assistant = agents.voice.Agent(
            instructions=instructions,
            stt=groq.STT(model="whisper-large-v3"),
            llm=groq.LLM(model="llama-3.3-70b-versatile"),
            tts=elevenlabs.TTS(),
        )
        print("  ✓ Voice agent instantiated successfully")
        print(f"  ✓ Agent type: {type(assistant).__name__}\n")
        return True
    except Exception as e:
        print(f"  ✗ Error instantiating agent: {e}\n")
        return False


def test_plugin_initialization():
    """Test that plugins can be initialized"""
    print("Testing plugin initialization...")
    
    try:
        stt = groq.STT(model="whisper-large-v3")
        print(f"  ✓ Groq STT initialized: {type(stt).__name__}")
        
        llm = groq.LLM(model="llama-3.3-70b-versatile")
        print(f"  ✓ Groq LLM initialized: {type(llm).__name__}")
        
        tts = elevenlabs.TTS()
        print(f"  ✓ ElevenLabs TTS initialized: {type(tts).__name__}\n")
        return True
    except Exception as e:
        print(f"  ✗ Error initializing plugins: {e}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Voice Agent Test Suite")
    print("=" * 60 + "\n")
    
    tests_passed = 0
    tests_total = 4
    
    try:
        test_agent_imports()
        tests_passed += 1
    except AssertionError as e:
        print(f"  ✗ Import test failed: {e}\n")
    
    try:
        test_agent_structure()
        tests_passed += 1
    except AssertionError as e:
        print(f"  ✗ Structure test failed: {e}\n")
    
    if test_plugin_initialization():
        tests_passed += 1
    
    if test_agent_instantiation():
        tests_passed += 1
    
    print("=" * 60)
    print(f"Test Results: {tests_passed}/{tests_total} tests passed")
    print("=" * 60)
    
    if tests_passed == tests_total:
        print("\n✓ All tests passed! The voice agent is properly configured.")
        print("\nNext steps:")
        print("1. Set up real API keys in .env.local")
        print("2. Configure LiveKit server credentials")
        print("3. Run: python agent.py start")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
