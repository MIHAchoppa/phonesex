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
- **💳 Monetization System**: Full payment processing, subscription management, and premium features
  - Three subscription tiers: FREE, PREMIUM, VIP
  - Secure Stripe payment integration
  - Usage tracking and limits
  - Feature gating for premium content

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
- `/plans` - View subscription plans (if monetization enabled)
- `/upgrade` - Get upgrade information (if monetization enabled)
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

### Monetization Configuration (Optional)

- `STRIPE_API_KEY` - Your Stripe API key for payment processing
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret for secure webhooks
- `STRIPE_TEST_MODE` - Set to 'true' for testing (default: true)
- `USER_DATA_DIR` - Directory for user data storage (default: ./user_data)

For detailed monetization setup, see [MONETIZATION.md](MONETIZATION.md)

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
