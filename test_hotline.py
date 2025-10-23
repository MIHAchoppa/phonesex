#!/usr/bin/env python3
"""
Basic tests for the AI Adult Hotline
"""
import os
import sys
from unittest.mock import Mock, patch
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from hotline import AdultHotline


class TestAdultHotline(unittest.TestCase):
    """Test cases for AdultHotline class"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('hotline.OpenAI')
    def test_initialization(self, mock_openai):
        """Test hotline initialization"""
        hotline = AdultHotline()
        self.assertIsNotNone(hotline.client)
        self.assertEqual(len(hotline.conversation_history), 0)
        
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        """Test error handling when API key is missing"""
        with self.assertRaises(ValueError):
            AdultHotline()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('hotline.OpenAI')
    def test_start_conversation(self, mock_openai):
        """Test conversation initialization"""
        hotline = AdultHotline()
        hotline.start_conversation()
        self.assertEqual(len(hotline.conversation_history), 1)
        self.assertEqual(hotline.conversation_history[0]['role'], 'system')
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('hotline.OpenAI')
    def test_get_response(self, mock_openai):
        """Test getting AI response"""
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hello! How can I help you?"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        hotline = AdultHotline()
        hotline.start_conversation()
        
        response = hotline.get_response("Hi there")
        
        self.assertEqual(response, "Hello! How can I help you?")
        self.assertEqual(len(hotline.conversation_history), 3)  # system + user + assistant


if __name__ == '__main__':
    unittest.main()
