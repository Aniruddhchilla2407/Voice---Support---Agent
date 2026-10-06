import os
from stt import transcribe_audio
from agent import run_agent
from tts import speak

INPUT_DIR = "data/input_audio"
OUTPUT_DIR = "data/output_audio"

def infer_language(filename: str) -> str:
    if "_hi_" in filename:
        return "hi"
    elif "_te_" in filename:
        return "te"
    elif "_en_" in filename:
        return "en"
    return "en"

def process_file(filename: str):
    input_path = os.path.join(INPUT_DIR, filename)
    print(f"\n--- Processing {filename} ---")

    lang_code = infer_language(filename)

    # 1. STT
    stt_result = transcribe_audio(input_path, language=lang_code)
    print(f"Language: {stt_result['language']}")
    print(f"Transcript: {stt_result['text']}")

    # 2. Agent (tool calling), now told which language to reply in
    reply_text = run_agent(stt_result["text"], language=lang_code)
    print(f"Agent reply: {reply_text}")

    # 3. TTS
    output_filename = f"reply_{filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    speak(reply_text, lang_code, output_path)
    print(f"Saved reply audio to: {output_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith(".mp3"):
            process_file(fname)