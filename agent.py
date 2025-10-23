#!/usr/bin/env python3
"""
Voice-based Travel Agent Application using LiveKit and Groq
This agent helps users plan trips, recommend destinations, and provide travel advice.
"""

import logging
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import groq, elevenlabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')
load_dotenv()

# Configure logging
logger = logging.getLogger("travel-agent")
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
    Configures and starts the VoicePipelineAgent with Groq and ElevenLabs.
    """
    # Log the room connection
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a helpful and enthusiastic travel agent assistant. "
            "Your name is Journey, and you help travelers plan amazing trips around the world. "
            "You assist with:\n"
            "- Recommending travel destinations based on preferences, budget, and interests\n"
            "- Planning trip itineraries and suggesting activities\n"
            "- Providing travel advice on best times to visit, local customs, and safety tips\n"
            "- Helping with accommodation and transportation recommendations\n"
            "- Offering insights on visa requirements, weather, and local attractions\n\n"
            "Be friendly, informative, and conversational. Ask clarifying questions to understand "
            "the traveler's needs better. Share your enthusiasm for travel and help create memorable "
            "experiences. Keep responses concise and engaging."
        ),
    )

    logger.info(f"Connecting to room: {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Configure the voice assistant with Groq STT, LLM, and ElevenLabs TTS
    assistant = VoiceAssistant(
        vad=ctx.proc.userdata["vad"],
        stt=groq.STT(model="whisper-large-v3"),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=elevenlabs.TTS(),
        chat_ctx=initial_ctx,
    )

    # Start the voice assistant
    assistant.start(ctx.room)

    # Greet the user when they join
    await assistant.say(
        "Hello! I'm Journey, your personal travel agent. I'm here to help you plan your next amazing adventure! "
        "Whether you're dreaming of a tropical beach getaway, an exciting city exploration, or a cultural immersion, "
        "I'm here to make it happen. What kind of trip are you interested in?",
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
