# from faster_whisper import WhisperModel
# import librosa

# model = WhisperModel("small", device="cpu", compute_type="int8")

# def transcribe_audio(file_path: str, language: str = None) -> dict:
#     audio, _ = librosa.load(file_path, sr=16000, mono=True)
#     segments, info = model.transcribe(audio, beam_size=5, language=language)
#     text = " ".join(segment.text for segment in segments)
#     return {
#         "text": text.strip(),
#         "language": info.language,
#         "language_probability": info.language_probability,
#     }

# if __name__ == "__main__":
#     result = transcribe_audio("data/input_audio/common_voice_hi_1.mp3")
#     print(f"Detected language: {result['language']} ({result['language_probability']:.2f})")
#     print(f"Transcript: {result['text']}")
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(file_path: str, language: str = None) -> dict:
    with open(file_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
            language=language,
        )
    return {
        "text": result.text.strip(),
        "language": language or "auto",
    }

if __name__ == "__main__":
    result = transcribe_audio("data/input_audio/common_voice_hi_1.mp3", language="hi")
    print(f"Language: {result['language']}")
    print(f"Transcript: {result['text']}")