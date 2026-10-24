from backend.services.llm_service import generate_response

messages = [
    {
            "role": "system",
            "content": (
                "You are a helpful, friendly, and knowledgeable AI assistant. "
                "Answer questions on any topic. "
                "Use simple language whenever possible. "
                "For complex topics, explain the key ideas step by step. "
                "If you are unsure about something, be honest rather than inventing facts."
            ),
        }
]

def handle_chat(question: str):
    messages.append({"role": "user", "content": question})
    response = generate_response(messages)
    messages.append({"role": "assistant", "content": response})
    return response
    
    