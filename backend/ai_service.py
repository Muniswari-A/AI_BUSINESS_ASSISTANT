import ollama

from backend.config import OLLAMA_MODEL
from prompts.prompt_builder import build_prompt


async def generate_response(
    message: str,
    context: str = ""
) -> str:

    prompt = build_prompt(
        user_message=message,
        context=context
    )

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
