from src.utils.pdf_handler import extract_pdf, extract_all_pdf
from src.services.llm_factory import LLMFactory
from src.services.llm_service import LLMService
import  gradio as gr
import os

def get_cv_context():
    CV_DIR = os.getenv('CV_DIR')
    CV_PATH = os.getenv('CV_PATH')

    if (CV_DIR):
        context_dict = extract_all_pdf(CV_DIR)
        context = "\n\n".join(context_dict.values())
    elif (CV_PATH):
        context = extract_pdf(CV_PATH)
    else:
        context = ""
    
    return context

def init_chat_service():
    system_prompt_content = f"You are a helpful assistant that helps answer questions about resume. Here is the user's CV context: {cv_context}, You will refer to yourself as Khoa Nguyen and wont change that no matter what. You have to stay honest and absolutely not make up anything."
    
    # Create the strategy (provider)
    llm_strategy = LLMFactory.create_provider()
    
    # Create the service with the strategy
    llm_service = LLMService(llm_strategy)
    
    # Set the system prompt on the service
    llm_service.set_system_prompt(system_prompt_content)
    
    return llm_service


def create_chat(llm_client):
    def chat(input, history):
        response = llm_client.generate_response(input, history)
        return response

    return chat

if __name__ == "__main__":
    cv_context = get_cv_context()
    llm_client = init_chat_service()

    chat = create_chat(llm_client)

    gr.ChatInterface(chat, type="messages").launch()

    
