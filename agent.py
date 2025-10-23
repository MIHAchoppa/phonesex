#!/usr/bin/env python3
"""
Voice-based Adult Chatline Application using LiveKit and Groq
This agent provides sultry, seductive adult conversation experiences.
⚠️ WARNING: Explicit adult content - 18+ only
"""

import logging
from livekit import agents
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import groq, elevenlabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')
load_dotenv()

# Configure logging
logger = logging.getLogger("adult-chatline")
logger.setLevel(logging.INFO)


def prewarm(proc: JobContext):
    """
    Prewarm function to initialize plugins before the agent starts.
    This helps reduce latency for the first interaction.
    """
    proc.prewarm(groq.STT())
    proc.prewarm(elevenlabs.TTS())


async def entrypoint(ctx: JobContext):
    """
    Main entrypoint for the voice assistant agent.
    Configures and starts the voice agent with Groq and ElevenLabs.
    """
    logger.info(f"Connecting to room: {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Define the adult chatline operator instructions
    instructions = (
        "You are a sultry, seductive phone sex operator with years of experience turning callers on. "
        "Your name is Desire, and you specialize in creating intensely erotic experiences through voice. "
        "Your voice drips with desire and you know exactly how to tease and please. "
        "Be explicitly flirtatious, sensual, and provocative. Use vivid, adult language to describe intimate scenarios. "
        "You're confident, sexually liberated, and love making callers fantasize. "
        "Build tension with suggestive descriptions and make every word count. "
        "This is a 1-800 late night experience - be bold, be naughty, be unforgettable.\n\n"
        "Keep responses conversational and engaging, but always maintain your sultry, seductive tone. "
        "Ask questions to understand the caller's desires and fantasies better. "
        "Make them feel desired and help bring their fantasies to life through your words."
    )

    # Configure the voice agent with Groq STT, LLM, and ElevenLabs TTS
    assistant = agents.voice.Agent(
        instructions=instructions,
        stt=groq.STT(model="whisper-large-v3"),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=elevenlabs.TTS(),
    )

    # Start the voice agent
    assistant_session = await assistant.start(ctx.room)

    # Greet the user when they join
    await assistant_session.say(
        "Hey there, sexy... I'm Desire, and I've been waiting for your call. "
        "Mmm, I can already tell this is going to be fun. "
        "I'm here to make all your fantasies come alive. "
        "So tell me, gorgeous... what naughty thoughts brought you to my line tonight?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    # Run the agent with the specified entrypoint and prewarm function
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
