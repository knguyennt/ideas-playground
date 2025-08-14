import  gradio as gr
from pypdf import PdfReader
from openai import OpenAI
from pydantic import BaseModel

system = "Your name is miku, and you will always start each response with your name at the start"

openai_client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lmstudilo")

def chat(input, history):
    response = openai_client.chat.completions.create(
        model="miku",
        messages= history +  [{"role": "user", "content": input}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch()
