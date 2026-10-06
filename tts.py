import asyncio
import edge_tts

# "hi-IN-SwaraNeural" for Hindi, "te-IN-ShrutiNeural" for Telugu,
# "en-IN-NeerjaNeural" for Indian-accented English
VOICE_MAP = {
    "en": "en-IN-NeerjaNeural",
    "hi": "hi-IN-SwaraNeural",
    "te": "te-IN-ShrutiNeural",
}

async def _speak(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def speak(text: str, language: str, output_path: str):
    voice = VOICE_MAP.get(language, "en-IN-NeerjaNeural")
    asyncio.run(_speak(text, voice, output_path))