# 🔥 Adult Chatline - Powered by GROQ AI

An AI-powered adult chatline application featuring ultra-fast, streaming conversations using GROQ's high-performance LLM API.

## Features

- **Ultra-Fast Responses**: Powered by GROQ's LPU technology for 300+ tokens/second
- **Real-Time Streaming**: Watch responses appear in real-time for natural conversations
- **Multiple AI Personalities**: Choose from 5 different conversation styles:
  - 💋 Flirty - Playful and charming
  - ❤️ Romantic - Sweet and affectionate
  - 🎭 Adventurous - Bold and daring
  - 🌙 Mysterious - Intriguing and enigmatic
  - 🎉 Playful - Fun and entertaining
- **Conversation History**: Maintains context throughout your session
- **Easy Configuration**: Simple environment-based setup
- **Interactive Commands**: Control the experience with built-in commands

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/MIHAchoppa/phonesex.git
cd phonesex
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your GROQ API key**:
   - Get your free API key from [console.groq.com](https://console.groq.com/)
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API key:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```

## Usage

Run the chatline:
```bash
python chatline.py
```

### Available Commands

- `/personalities` - List and change AI personalities
- `/clear` - Clear conversation history
- `/stats` - Show conversation statistics
- `/help` - Show help menu
- `/quit` - Exit the chatline

### Example Session

```
🔥 ADULT CHATLINE - Powered by GROQ AI 🔥
Current personality: Flirty

You: Hey there!
AI: Well hello there, gorgeous! I've been waiting for someone interesting 
like you to come along... 😉 What brings you to my corner of the world 
tonight?

You: /personalities
✨ Available Personalities:
  ★ 1. Flirty
    2. Romantic
    3. Adventurous
    4. Mysterious
    5. Playful

You: Just want to chat
AI: Oh, I love a good chat! Especially with someone who knows what they 
want. Tell me, what's been on your mind lately? I'm all ears... and maybe 
a little more 😘
```

## Configuration

Edit `.env` to customize:

- `GROQ_API_KEY` - Your GROQ API key (required)
- `AI_MODEL` - Model to use (default: llama-3.1-70b-versatile)
- `TEMPERATURE` - Response creativity (0.0-1.0, default: 0.8)
- `MAX_TOKENS` - Maximum response length (default: 1024)

### Available Models

GROQ supports many high-performance models for different use cases:

#### Llama 3.3 Models (Latest)
- `llama-3.3-70b-versatile` - Latest versatile 70B model with enhanced capabilities
- `llama-3.3-70b-specdec` - Speculative decoding version for faster inference

#### Llama 3.2 Models
- `llama-3.2-1b-preview` - Ultra-lightweight 1B model for fastest responses
- `llama-3.2-3b-preview` - Compact 3B model balancing speed and quality
- `llama-3.2-11b-vision-preview` - Vision-capable 11B model
- `llama-3.2-90b-vision-preview` - High-performance 90B vision model

#### Llama 3.1 Models
- `llama-3.1-70b-versatile` - Excellent overall performance (recommended default)
- `llama-3.1-8b-instant` - Ultra-fast 8B model for instant responses

#### Llama 3 Models
- `llama3-70b-8192` - Original Llama 3 70B with 8K context
- `llama3-8b-8192` - Original Llama 3 8B with 8K context
- `llama3-groq-70b-8192-tool-use-preview` - Tool use optimized 70B
- `llama3-groq-8b-8192-tool-use-preview` - Tool use optimized 8B

#### Security & Moderation
- `llama-guard-3-8b` - Content moderation and safety model

#### Mixtral Models
- `mixtral-8x7b-32768` - Mixture of experts with 32K context window

#### Gemma Models (Google)
- `gemma-7b-it` - Google's efficient 7B instruction-tuned model
- `gemma2-9b-it` - Latest Gemma 2 9B instruction-tuned model

#### Audio Models (Whisper)
- `whisper-large-v3` - High-quality audio transcription
- `whisper-large-v3-turbo` - Faster audio transcription
- `distil-whisper-large-v3-en` - Distilled English-only transcription

**Recommended Models for Chatline:**
- **Best Overall**: `llama-3.3-70b-versatile` or `llama-3.1-70b-versatile`
- **Fastest**: `llama-3.2-1b-preview` or `llama-3.1-8b-instant`
- **Long Context**: `mixtral-8x7b-32768` (32K tokens)
- **Efficient**: `gemma2-9b-it` or `gemma-7b-it`

## Technical Details

### GROQ Integration

This application leverages GROQ's advanced features:
- **Streaming API**: Real-time token streaming for natural conversation flow
- **Low Latency**: Sub-second response times using LPU hardware
- **Conversation Context**: Full message history management
- **Flexible Models**: Support for multiple open-weight LLMs

### Architecture

- Built with Python 3.8+
- Uses official GROQ Python SDK
- Environment-based configuration
- Modular personality system
- Stateful conversation management

## Requirements

- Python 3.8 or higher
- GROQ API key (free tier available)
- Internet connection

## Privacy & Safety

- Conversations are not stored locally
- API calls follow GROQ's privacy policy
- No personal data is collected by this application
- Users must be 18+ years old

## License

This project is provided as-is for educational and entertainment purposes.

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## Support

For issues or questions:
- Open an issue on GitHub
- Check GROQ documentation at [console.groq.com/docs](https://console.groq.com/docs)
