import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
    
messages = []

def main():
    while True:
        user_input = input("User:")
        messages.append({'role': 'user', 'content': user_input})
        if user_input.lower() == "bye":
            print("Exiting the chat. Goodbye!")
            break
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            stream=True
        )
        assistant_message = ""
        print("Assistant: ", end="")
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            assistant_message += content
           
            print(content, end="", flush=True)
           
        print()
            
            
        
        messages.append({'role': 'assistant', 'content': assistant_message})
        
if __name__ == "__main__":
    main()