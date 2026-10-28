import logging
import os

from dotenv import load_dotenv
from groq import Groq

logger = logging.getLogger(__name__)

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_response(messages):
    logger.info("Sending message to LLM.")
    try:
        response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
            # stream=True,
            )
        answer = response.choices[0].message.content
        logger.info("Successfully received response from LLM")
        return answer
    
    except Exception:
        logger.exception("Failed to generate response from LLM.")
        raise

    