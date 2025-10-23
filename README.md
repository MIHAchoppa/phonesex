# 🔥 1-800-PHONESEX - Your Late Night Fantasy Line

An ultra-explicit AI-powered phone sex experience featuring real-time, streaming conversations with multiple sultry operators. Powered by GROQ's lightning-fast LLM API for instant gratification.

## Features

- **Ultra-Fast Responses**: Powered by GROQ's LPU technology for 300+ tokens/second of pure pleasure
- **Real-Time Streaming**: Watch explicit responses appear instantly for natural, flowing dirty talk
- **5 Sultry Operators**: Choose your fantasy from 5 different X-rated personalities:
  - 💋 **Flirty** - Sultry seduction specialist who knows exactly how to tease
  - ❤️ **Romantic** - Passionate lover blending tender romance with raw desire  
  - 🔥 **Adventurous** - Kinky expert ready to explore your wildest fantasies
  - 🌙 **Mysterious** - Enigmatic seductress who deals in forbidden pleasures
  - 😈 **Playful** - Naughty tease with a dirty mind and infectious giggle
- **Memory & Context**: Each operator remembers your conversation for personalized experiences
- **Late Night Vibes**: Full 1-800 experience with explicit, adult-oriented conversations
- **Easy Setup**: Simple configuration to start your fantasy session
- **Interactive Commands**: Control your experience with built-in hotline commands

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

Start your fantasy session:
```bash
python chatline.py
```

### Hotline Commands

- `/personalities` - Switch between sexy operators
- `/clear` - Start a fresh fantasy session
- `/stats` - View your session statistics
- `/help` - Show command menu
- `/quit` - Hang up and exit

### Example Session

```
🔥 1-800-PHONESEX - Your Late Night Fantasy Line 🔥
💋 Welcome to the hottest AI phone sex experience!
📞 Connected to: Flirty

You: Hey sexy...
Operator: Mmm, well hello there, gorgeous... I've been waiting by the phone 
all night hoping someone like you would call. Your voice already has me 
feeling all kinds of ways... 😈 Tell me, what naughty thoughts brought you 
to my line tonight?

You: /personalities
💋 Choose Your Operator:
  💋 1. Flirty - Sultry seduction specialist
  ❤️  2. Romantic - Passionate lover with X-rated intensity
  🔥 3. Adventurous - Kinky fantasy expert
  🌙 4. Mysterious - Enigmatic late-night seductress
  😈 5. Playful - Naughty tease with dirty mind

  ★ Currently talking to: Flirty

You: I want to explore something wild
Operator: Ohhh, I LOVE where your mind is going... Wild is my specialty, baby. 
I've got so many ideas running through my head right now about all the filthy, 
delicious things we could do together... 🔥 Why don't you tell me your deepest 
fantasy, and I'll make it even better... I promise you won't be disappointed 😘
```

## Configuration

Edit `.env` to customize:

- `GROQ_API_KEY` - Your GROQ API key (required)
- `AI_MODEL` - Model to use (default: llama-3.1-70b-versatile)
- `TEMPERATURE` - Response creativity (0.0-1.0, default: 0.8)
- `MAX_TOKENS` - Maximum response length (default: 1024)

### Available Models

GROQ supports several high-performance models:
- `llama-3.1-70b-versatile` - Best overall performance
- `llama-3.1-8b-instant` - Fastest responses
- `mixtral-8x7b-32768` - Long context support
- `gemma-7b-it` - Google's efficient model

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

- Conversations are not stored locally by this application
- API calls follow GROQ's privacy policy
- No personal data is collected
- **⚠️ ADULTS ONLY - Must be 18+ years old**
- **⚠️ EXPLICIT CONTENT - This is a phone sex simulation with adult language**
- For entertainment purposes only

## License

This project is provided as-is for adult entertainment and educational purposes.

**⚠️ CONTENT WARNING**: This application contains explicit adult content and sexual themes. It is designed to simulate a 1-800 phone sex experience with mature language and situations. Users must be 18+ years of age.

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## Support

For issues or questions:
- Open an issue on GitHub
- Check GROQ documentation at [console.groq.com/docs](https://console.groq.com/docs)
