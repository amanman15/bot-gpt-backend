from groq import Groq
from dotenv import load_dotenv
import os
from groq import GroqError


load_dotenv()
client = Groq()

async def call_llm(messages_list):
    try:
        messages_payload = []
        for msg in messages_list:
            if isinstance(msg, str):
                messages_payload.append({"role": "user", "content": msg})
            elif isinstance(msg, dict):
                messages_payload.append(msg)
            else:
                raise ValueError("Each message must be str or dict")

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages_payload,
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            reasoning_effort="medium",
            stream=False
        )

        return completion.choices[0].message.content

    except GroqError as e:
        # LLM provider error
        raise RuntimeError(f"LLM call failed: {str(e)}")

    except Exception as e:
        raise RuntimeError(f"Unexpected LLM error: {str(e)}")
