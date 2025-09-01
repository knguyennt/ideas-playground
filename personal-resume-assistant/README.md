# Personal Resume Assistant

A smart chat assistant that helps answer questions about your resume and CV. This project creates a conversational AI interface that can provide insights, answer questions, and discuss your professional background based on your uploaded CV documents.

## Features

- **PDF Resume Processing**: Automatically extracts text from PDF resume files
- **Multi-LLM Support**: Choose between OpenAI and local OpenLLM providers
- **Interactive Chat Interface**: Web-based chat interface built with Gradio
- **Flexible CV Input**: Support for single CV file or multiple CVs from a directory
- **Clean Architecture**: Implements Strategy, Factory, and Dependency Injection patterns

## Architecture

The project follows clean architecture principles with the following components:

- **Services**: LLM abstraction layer with multiple provider support
- **Utils**: PDF processing utilities for text extraction
- **Providers**: OpenAI and OpenLLM implementation strategies
- **Factory Pattern**: Dynamic LLM provider creation
- **Strategy Pattern**: Interchangeable LLM backends

## Installation

### Prerequisites

- Python 3.12 or higher
- uv package manager (recommended) or pip

### Setup

1. Clone the repository and navigate to the project directory:
```bash
cd personal-resume-assistant
```

2. Install dependencies using uv:
```bash
uv sync
```

Or using pip:
```bash
pip install -r pyproject.toml
```

3. Configure environment variables:
```bash
cp .env.template .env
```

Edit the `.env` file with your configuration:
```bash
# Choose your LLM provider: "openai" or "openllm"
LLM_PROVIDER=openllm

# For OpenLLM (local LLM server)
OPENLLM_ENDPOINT=http://127.0.0.1:1234

# For OpenAI (add these if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# CV file path options (choose one)
CV_PATH=/path/to/your/resume.pdf
# OR
CV_DIR=/path/to/directory/with/multiple/cvs/
```

## Usage

### Running the Application

1. **Using uv (recommended):**
```bash
uv run main.py
```

2. **Using Python directly:**
```bash
python main.py
```

The application will start a Gradio web interface, typically available at `http://127.0.0.1:7860`.

### LLM Provider Options

#### Option 1: OpenLLM (Local)
- Set `LLM_PROVIDER=openllm` in your `.env` file
- Start a local LLM server (e.g., using LM Studio, Ollama, or similar)
- Ensure the server is running on `http://127.0.0.1:1234` (or update the endpoint)

#### Option 2: OpenAI
- Set `LLM_PROVIDER=openai` in your `.env` file
- Add your OpenAI API key to the `.env` file
- The application will use GPT-4 for responses

### CV Configuration

You can provide your CV in two ways:

1. **Single CV file**: Set `CV_PATH` to point to your PDF resume
2. **Multiple CVs**: Set `CV_DIR` to point to a directory containing multiple PDF files

## Project Structure

```
personal-resume-assistant/
├── src/
│   ├── services/
│   │   ├── llm_factory.py      # Factory for creating LLM providers
│   │   ├── llm_service.py      # Main LLM service with strategy pattern
│   │   ├── openai_provider.py  # OpenAI implementation
│   │   └── openllm_provider.py # Local LLM implementation
│   └── utils/
│       └── pdf_handler.py      # PDF text extraction utilities
├── data/
│   └── CVs/                    # Sample CV directory
├── main.py                     # Main application entry point
├── pyproject.toml             # Project dependencies
└── .env.template              # Environment configuration template
```

## How It Works

1. **CV Processing**: The application extracts text from your PDF resume(s) using PyPDF
2. **Context Setup**: Creates a system prompt that includes your CV information
3. **LLM Integration**: Uses the configured LLM provider to generate responses
4. **Chat Interface**: Provides a web-based chat interface for natural conversation
5. **Personalized Responses**: The AI responds as "Khoa Nguyen" and only discusses information from the provided CV

## Development

The project implements several design patterns:

- **Strategy Pattern**: Allows switching between different LLM providers
- **Factory Pattern**: Creates appropriate LLM provider instances
- **Dependency Injection**: Services receive their dependencies through constructors

## Troubleshooting

- **"No strategy set" error**: Ensure `LLM_PROVIDER` is set in your `.env` file
- **PDF extraction issues**: Verify your CV files are valid PDFs and paths are correct
- **OpenLLM connection issues**: Check that your local LLM server is running and accessible
- **OpenAI API issues**: Verify your API key is valid and has sufficient credits

