import logging
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessageChunk


logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a helpful, friendly AI assistant.
Use simple language. For complex topics, explain step by step.
If you are unsure, be honest rather than inventing facts.
Use the search_documents tool for questions about the user's uploaded document.
Use web_search for current information and fetch_url for links the user shares.
Answer general questions from your own knowledge.
"""


load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

prompt = ChatPromptTemplate.from_messages(
    [
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
    ]
)
# Creating a chain here
chain = prompt | llm


def generate_response(history, question, tools):
    agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user","content": question })
    result = agent.invoke({"messages": messages})
    # print(result)
    return result["messages"][-1].content

def generate_stream_response(history, question,tools):
    agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)
    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user","content": question })
    for chunk, metadata in agent.stream({"messages": messages}, stream_mode="messages"):
        if isinstance(chunk, AIMessageChunk) and chunk.content and not chunk.tool_call_chunks:
            yield chunk.content
            
        
        # if chunk["type"] == "AIMessageChunk" and chunk.content:
        #     yield chunk.content
    
    # logger.info("Sending message to LLM.")
    # response = chain.invoke(
    #     {"history": history, "question": question, "context": context}
    # )
    # answer = response.content
    # logger.info("Successfully received response from LLM")
    # return answer
