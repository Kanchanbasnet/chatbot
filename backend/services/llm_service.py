import logging
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
            You are a helpful, friendly, and knowledgeable AI assistant. 
            Answer questions on any topic. 
            Use simple language whenever possible. 
            For complex topics, explain the key ideas step by step. 
            If you are unsure about something, be honest rather than inventing facts.
        """


load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    (
        "human",
        """
        Context from external sources, if provided:
        {context}

        Question:
        {question}
        """,
    ),
])
# Creating a chain here
chain = prompt | llm


def generate_response(history, question, context=""):
    logger.info("Sending message to LLM.")
    response = chain.invoke({"history": history, "question": question, "context": context})
    answer = response.content
    logger.info("Successfully received response from LLM")
    return answer
