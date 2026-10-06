import json
import os
from groq import Groq
from dotenv import load_dotenv
from tools import TOOLS_SCHEMA, AVAILABLE_FUNCTIONS

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANG_NAMES = {"hi": "Hindi", "te": "Telugu", "en": "English"}

def run_agent(user_text: str, language: str = "en") -> str:
    lang_name = LANG_NAMES.get(language, "the same language as the user")

    messages = [
        {
            "role": "system",
            "content": (
                f"You are a helpful voice assistant. Always reply in {lang_name}, "
                "regardless of what language you think in. Use tools when needed. "
                "Keep answers short and conversational, suitable for being spoken aloud."
            ),
        },
        {"role": "user", "content": user_text},
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=TOOLS_SCHEMA,
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = AVAILABLE_FUNCTIONS[func_name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
        )
        return final_response.choices[0].message.content

    return msg.content