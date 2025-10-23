# Voice Agent Setup Guide

## Overview

This repository now includes a voice-based travel agent application built with LiveKit and Groq. The agent uses real-time voice interaction to help users plan trips and get travel recommendations.

## Architecture

The voice agent consists of three main components:

1. **Speech-to-Text (STT)**: Groq's `whisper-large-v3` model converts user speech to text
2. **Language Model (LLM)**: Groq's `llama-3.3-70b-versatile` processes requests and generates responses
3. **Text-to-Speech (TTS)**: ElevenLabs synthesizes natural-sounding voice responses

## Prerequisites

1. **Python 3.8+** - The agent requires Python 3.8 or higher
2. **LiveKit Account** - Sign up at https://cloud.livekit.io/ for free
3. **Groq API Key** - Get yours from https://console.groq.com/
4. **ElevenLabs API Key** - Sign up at https://elevenlabs.io/

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `livekit-agents>=0.9.0` - Core LiveKit agents framework
- `livekit-plugins-groq>=0.1.0` - Groq integration for STT and LLM
- `livekit-plugins-elevenlabs>=0.7.9` - ElevenLabs integration for TTS
- `groq>=0.4.0` - Groq Python SDK
- `python-dotenv>=1.0.0` - Environment variable management

### 2. Configure Environment Variables

Copy the example configuration:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your credentials:

```bash
# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key

# ElevenLabs API Configuration
ELEVEN_API_KEY=your_elevenlabs_api_key

# Optional: Override default models
AI_MODEL=llama-3.3-70b-versatile
STT_MODEL=whisper-large-v3
```

### 3. Test the Installation

Run the test suite to verify everything is configured correctly:

```bash
python test_agent.py
```

You should see:
```
✓ All tests passed! The voice agent is properly configured.
```

### 4. Start the Agent

Run the voice agent:

```bash
python agent.py start
```

The agent will:
1. Connect to your LiveKit server
2. Wait for users to join the room
3. Greet users with an introduction
4. Listen to voice input and respond naturally

## Agent Features

The travel agent "Journey" can help with:

- **Destination Recommendations**: Suggests places based on preferences, budget, and interests
- **Trip Planning**: Creates itineraries and suggests activities
- **Travel Advice**: Provides information on timing, customs, and safety
- **Accommodation Help**: Recommends hotels and lodging options
- **Transportation**: Advises on getting around destinations
- **Practical Info**: Visa requirements, weather forecasts, and local attractions

## File Structure

```
phonesex/
├── agent.py              # Main voice agent implementation
├── test_agent.py         # Test suite for the agent
├── requirements.txt      # Python dependencies
├── .env.local           # Environment configuration (not committed)
├── .env.example         # Example environment file
└── README.md            # Main project documentation
```

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### API Key Errors

Make sure your `.env.local` file contains valid API keys:

```bash
# Check that your file exists
cat .env.local

# Verify the keys are set (don't share the output!)
python -c "from dotenv import load_dotenv; import os; load_dotenv('.env.local'); print('GROQ_API_KEY:', 'SET' if os.getenv('GROQ_API_KEY') else 'NOT SET')"
```

### Connection Issues

If the agent can't connect to LiveKit:

1. Verify your `LIVEKIT_URL` is correct
2. Check your `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`
3. Ensure your LiveKit project is active

## Development

### Customizing the Agent

The agent's personality and capabilities can be customized in `agent.py`:

```python
# Modify the instructions to change the agent's behavior
instructions = (
    "You are a helpful and enthusiastic travel agent assistant. "
    "Your name is Journey..."
)
```

### Changing Models

Update the models in the agent configuration:

```python
assistant = agents.voice.Agent(
    instructions=instructions,
    stt=groq.STT(model="whisper-large-v3"),  # Change STT model
    llm=groq.LLM(model="llama-3.3-70b-versatile"),  # Change LLM model
    tts=elevenlabs.TTS(),  # Configure TTS options
)
```

## Next Steps

### Frontend Integration

To create a user interface for the voice agent:

1. Use the LiveKit Next.js template
2. Configure the frontend to connect to your LiveKit server
3. Implement UI controls for starting/stopping the conversation
4. Add visual feedback for speech recognition and agent responses

### Production Deployment

For production use:

1. Set up a dedicated LiveKit server or use LiveKit Cloud
2. Configure proper authentication and authorization
3. Implement rate limiting and usage tracking
4. Monitor agent performance and costs
5. Set up logging and error tracking

## Security Considerations

- Never commit `.env.local` or any file containing API keys
- Use environment variables for all sensitive configuration
- Rotate API keys regularly
- Monitor API usage to detect unauthorized access
- Implement proper authentication for production deployments

## Support

For issues or questions:
- Check the LiveKit documentation: https://docs.livekit.io/
- Review Groq documentation: https://console.groq.com/docs
- Visit ElevenLabs docs: https://elevenlabs.io/docs
- Open an issue on GitHub

## License

This project is provided as-is for educational and development purposes.
