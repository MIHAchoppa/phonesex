# AI Adult Hotline

An AI-powered conversational adult chatline using OpenAI's GPT technology.

## Features

- Interactive conversational AI
- Natural language processing
- Respectful and engaging dialogue
- Command-line interface

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MIHAchoppa/phonesex.git
cd phonesex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Demo Mode (No API Key Required)

To see a demonstration of the hotline functionality:
```bash
python demo.py
```

### Live Mode (Requires API Key)

Run the hotline:
```bash
python hotline.py
```

Type your messages and press Enter to chat with the AI. Type `quit` or `exit` to end the conversation.

## Testing

Run the test suite:
```bash
python test_hotline.py -v
```

## Configuration

Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## License

This project is for educational and entertainment purposes.
