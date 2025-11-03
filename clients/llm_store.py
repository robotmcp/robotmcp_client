from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def _get_groq_llm(model_name):
    return ChatGroq(
        model=model_name,
        temperature=0.2,
        max_tokens=10240,
        api_key=os.getenv("GROQ_API_KEY"),
    )


def get_llm(llm_name):
    llms = {
        "gemini": "google_genai:gemini-2.5-flash-lite",
        "openai": "openai:gpt-4.1",
        "claude": "anthropic:claude-sonnet-4-5",
        "llama-scout": _get_groq_llm("llama-4-scout-17b-16e-instruct"),
        "llama-8b": _get_groq_llm("llama-3.1-8b-instant"),
        "llama": _get_groq_llm("llama-3.3-70b-versatile"),
        "gpt-oss": _get_groq_llm("openai/gpt-oss-120b"),
    }
    return llms[llm_name]
