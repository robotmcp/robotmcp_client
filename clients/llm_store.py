from langchain_cerebras import ChatCerebras
import os
from dotenv import load_dotenv

load_dotenv()


def _get_cerebras_llm(model_name):
    return ChatCerebras(
        model=model_name,
        temperature=0.2,
        max_tokens=10240,
        api_key=os.getenv("CEREBRAS_API_KEY"),
    )


def get_llm(llm_name):
    llms = {
        "gemini": "google_genai:gemini-2.5-flash-lite",
        "openai": "openai:gpt-4.1",
        "claude": "anthropic:claude-sonnet-4-5",
        "llama": _get_cerebras_llm("llama-3.3-70b"),
        "qwen": _get_cerebras_llm("qwen-3-32b"),
        "gpt-oss": _get_cerebras_llm("gpt-oss-120b"),
    }
    return llms[llm_name]
