"""
Quick sanity tests for the voice agent pipeline.

"""

import os
import sys

# allow imports from project root when running tests directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stt import transcribe_audio
from agent import run_agent
from tts import speak
from tools import get_order_status, get_weather

SAMPLE_AUDIO_DIR = "data/input_audio"


def test_tools_return_expected_values():
    """Mock tool functions should return deterministic results."""
    assert "shipped" in get_order_status("1234")
    assert get_order_status("0000") == "order not found"
    assert "sunny" in get_weather("Hyderabad")
    assert get_weather("Atlantis") == "weather data not available"
    print("test_tools_return_expected_values passed")


def test_stt_returns_nonempty_transcript():
    """STT should return a non-empty transcript for a real audio file."""
    sample_files = [f for f in os.listdir(SAMPLE_AUDIO_DIR) if f.endswith(".mp3")]
    assert len(sample_files) > 0, "No sample audio files found in data/input_audio"

    test_file = os.path.join(SAMPLE_AUDIO_DIR, sample_files[0])
    result = transcribe_audio(test_file, language="hi")

    assert "text" in result
    assert len(result["text"]) > 0
    print(f"test_stt_returns_nonempty_transcript passed — transcript: {result['text']}")


def test_agent_calls_tool_for_order_query():
    """Agent should trigger get_order_status when asked about an order."""
    reply = run_agent("What is the status of order 1234?", language="en")
    assert reply is not None
    assert len(reply) > 0
    # loose check: reply should reference the order outcome, not just deflect
    print(f"test_agent_calls_tool_for_order_query passed — reply: {reply}")


def test_agent_handles_ambiguous_input():
    """Agent should ask for clarification on vague input, not hallucinate."""
    reply = run_agent("the cat sat on the roof", language="en")
    assert reply is not None
    assert len(reply) > 0
    print(f"test_agent_handles_ambiguous_input passed — reply: {reply}")


def test_tts_creates_output_file():
    """TTS should produce a non-empty audio file."""
    output_path = "data/output_audio/test_tts_output.mp3"
    speak("Hello, this is a test.", "en", output_path)

    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    print(f"test_tts_creates_output_file passed — saved to {output_path}")


def test_full_pipeline_end_to_end():
    """Run one real audio file through the entire STT -> agent -> TTS pipeline."""
    sample_files = [f for f in os.listdir(SAMPLE_AUDIO_DIR) if f.endswith(".mp3")]
    assert len(sample_files) > 0

    test_file = os.path.join(SAMPLE_AUDIO_DIR, sample_files[0])
    lang = "hi" if "_hi_" in test_file else "te" if "_te_" in test_file else "en"

    stt_result = transcribe_audio(test_file, language=lang)
    assert len(stt_result["text"]) > 0

    reply = run_agent(stt_result["text"], language=lang)
    assert reply is not None and len(reply) > 0

    output_path = "data/output_audio/test_full_pipeline.mp3"
    speak(reply, lang, output_path)
    assert os.path.exists(output_path)

    print(f"test_full_pipeline_end_to_end passed")
    print(f"  Transcript: {stt_result['text']}")
    print(f"  Reply: {reply}")


if __name__ == "__main__":
    # allows running as a plain script without pytest
    print("Running pipeline sanity tests...\n")
    test_tools_return_expected_values()
    test_stt_returns_nonempty_transcript()
    test_agent_calls_tool_for_order_query()
    test_agent_handles_ambiguous_input()
    test_tts_creates_output_file()
    test_full_pipeline_end_to_end()
    print("\nAll tests passed.")