# Voice-Driven Support Agent

A voice agent that listens to a spoken question, understands intent, calls the right backend tool when needed, and replies back in natural speech — in the same language the user spoke.

Built as a demonstration of a full STT → LLM agent (with tool calling) → TTS pipeline, tested across English, Hindi, and Telugu.

## How it works

1. **Speech-to-Text**: Groq's hosted `whisper-large-v3-turbo` transcribes spoken audio into text.
2. **Agent reasoning**: The transcript is sent to an LLM (`openai/gpt-oss-20b` via Groq) with access to a small set of tools (`get_order_status`, `get_weather`). The model decides whether to call a tool based on what was actually asked, then composes a natural, spoken-style reply — always in the same language the user spoke in.
3. **Text-to-Speech**: The reply is converted back into spoken audio using `edge-tts`, with language-appropriate voices (e.g. Hindi, Telugu, Indian-accented English).

## Project structure
├── main.py              # orchestrates the full pipeline
├── stt.py                # speech-to-text (Groq Whisper)
├── tts.py                 # text-to-speech (edge-tts)
├── agent.py               # LLM + tool-calling loop
├── tools.py                # mock backend tools the agent can call
├── data/
│   ├── input_audio/        # sample voice clips (Common Voice dataset)
│   └── output_audio/       # generated spoken replies
└── tests/
    └── test_pipeline.py    # sanity tests for each component + full pipeline


## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your Groq API key:

GROQ_API_KEY=your_key_here


## Running

Process all audio clips in `data/input_audio/`:
```bash
python main.py
```

Run the test suite:
```bash
python -m pytest tests/test_pipeline.py -v
```

## Dataset

Sample input audio is drawn from [Mozilla Common Voice](https://commonvoice.mozilla.org/), covering Hindi and Telugu, to test transcription accuracy and conversational handling across Indian languages. A small set of clips (~15 per language) is included directly in `data/input_audio/` so the pipeline can be run immediately without downloading the full dataset.

## Notes

- Tool calling only triggers when the spoken input actually maps to a known tool (e.g. an order status or weather question). Ambiguous or unrelated input is handled by asking for clarification rather than hallucinating an answer.
- The architecture is language-agnostic — adding a new language mainly requires mapping it to an appropriate `edge-tts` voice in `tts.py`.  
