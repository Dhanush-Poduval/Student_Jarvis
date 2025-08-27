from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Fetch all voices
voices = client.voices.get_all()

for voice in voices.voices:
    print(f"Name: {voice.name}")
    print(f"Voice ID: {voice.voice_id}")
    print()
