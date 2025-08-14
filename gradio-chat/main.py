import  gradio as gr
from pypdf import PdfReader
from openai import OpenAI
from pydantic import BaseModel


def chat(input):
    return f"Hello {input}"

history = [
    gr.ChatMessage(role="assistant", content="How can I help you?"),
    gr.ChatMessage(role="user", content="Can you make me a plot of quarterly sales?"),
    gr.ChatMessage(role="assistant", content="I am happy to provide you that report and plot.")
]

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Chatbot(history, type="messages")
    demo.launch()
