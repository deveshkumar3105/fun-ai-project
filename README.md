# Fun AI Project

A hands-on playground for experimenting with modern AI workflows using LangChain, Google Generative AI, Groq, Ollama, and Streamlit. The project includes small interactive apps, research-style LLM agents, and notebook-based experiments for learning and prototyping.

## Overview

This repository is designed for exploring:

- LLM application patterns with LangChain
- Google Gemini integration via `langchain-google-genai`
- Groq-hosted models and fast inference
- Search-augmented question answering with Serper
- Local model usage through Ollama
- Streamlit UI prototypes for chat-based experiences
- Prompt engineering, memory, streaming, and structured outputs

## Project structure

- `apps/` — runnable AI demos and mini apps
  - `apps/1_qna_chatbot.py` — simple Streamlit Q&A chatbot using Google Generative AI
  - `apps/2_google_agent.py` — research assistant that decides when to search and answers with Groq + Google Search results
  - `apps/3_qna_chatbot_w_google_search.py` — streaming Streamlit chatbot with Google Search via Serper
  - `apps/4_sql_agent.py` — Streamlit task manager that uses a SQLite database and a Groq-backed SQL agent
- `notebooks/` — experiment notebooks covering multiple AI topics
  - `1_langcain_chatbot.ipynb`
  - `2_prompt_engg.ipynb`
  - `3_memory_management.ipynb`
  - `4_structured_output.ipynb`
  - `5_ollama_app.ipynb`
  - `6_groq_langchain_qwen.ipynb`
  - `7_streaming_response.ipynb`
  - `8_agent_initialization.ipynb`
  - `9_google_serper.ipynb`
- `requirements.txt` — Python dependencies used across the project
- `.env` — local environment file for API keys (not committed)
- `venv/` — local virtual environment

## Tech stack

- Python
- LangChain
- Google Generative AI / Gemini
- Groq
- Ollama
- Serper API
- Streamlit
- Rich (for console UI in terminal apps)
- Jupyter notebooks

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd fun-ai-proj
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

> Do not commit your `.env` file to version control.

## Run the apps

### Streamlit chatbot

```bash
streamlit run apps/1_qna_chatbot.py
```

This app creates a simple chat interface using LangChain and Google Gemini.

### Research assistant

```bash
python apps/2_google_agent.py
```

This script runs an interactive terminal-based assistant that:

- decides whether a query needs web search
- uses Serper to fetch current search results
- sends those results to Groq-backed LLM to generate an answer
- supports `quit` or `exit` to leave the session

### Search chatbot

```bash
streamlit run apps/3_qna_chatbot_w_google_search.py
```

This app combines a Groq model with Google Search results from Serper.

### SQL task manager

```bash
streamlit run apps/4_sql_agent.py
```

The app creates `my_tasks.db` in the directory where Streamlit is launched and creates a `tasks` table if one does not already exist. Tasks have a title, optional description, status (`pending`, `in_progress`, or `completed`), and creation timestamp. The SQL agent is instructed to list at most 10 tasks and verify create, update, and delete operations with a follow-up query.

The existing table is not altered when the app runs. If you change its schema, migrate or recreate the SQLite database as needed.

## Repository status

- Current branch: `main`
- Latest commit at the time of this update: `a158dc4` (`SQL DB Handler Agent`)
- Working tree was clean when checked.
- The project includes four runnable apps and nine exploratory notebooks.

## Notebook coverage

The notebooks in this project cover the following topics:

- `1_langcain_chatbot.ipynb` — basic chat bot patterns
- `2_prompt_engg.ipynb` — prompt engineering techniques
- `3_memory_management.ipynb` — memory in LLM apps
- `4_structured_output.ipynb` — structured responses and parsing
- `5_ollama_app.ipynb` — local LLM usage with Ollama
- `6_groq_langchain_qwen.ipynb` — Groq + LangChain + Qwen experiments
- `7_streaming_response.ipynb` — streaming output examples
- `8_agent_initialization.ipynb` — agent setup and configuration
- `9_google_serper.ipynb` — search-powered agent workflows

## Notes

- The project is intended as an experimentation and learning repo.
- Model names, API keys, and providers can be adjusted based on your setup.
- You can mix Google AI, Groq, and local Ollama models depending on your environment and desired use case.
- Search behavior is especially useful for questions that depend on current information.

## License

This repository is currently for experimentation and learning. Add an appropriate license if you plan to share or publish it publicly.
