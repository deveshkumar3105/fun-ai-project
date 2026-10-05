# fun-ai-project

Small playground for experimenting with LangChain, Google Generative AI, Ollama, and Streamlit-based demos.

## Structure

- `apps/` — Streamlit app demos, including the Q&A chatbot.
- `notebooks/` — Jupyter notebooks covering prompt engineering, memory, structured output, and local LLM workflows.
- `requirements.txt` — Python dependencies for the project.
- `venv/` — local virtual environment used during development.

## Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your secrets in a `.env` file (do NOT commit it):

```bash
GOOGLE_API_KEY=your_api_key_here
OTHER_SECRET=...
```

4. Run the Streamlit demo:

```bash
streamlit run apps/1_qna_chatbot.py
```

## Notebook coverage

Current examples include:

- `1_langcain_chatbot.ipynb`
- `2_prompt_engg.ipynb`
- `3_memory_management.ipynb`
- `4_structured_output.ipynb`
- `5_ollama_app.ipynb`

## Notes

- `.env` is listed in `.gitignore` to avoid accidentally committing credentials.
- Replace model names and API keys as needed for your account.
- The project can be used with both Google GenAI and local Ollama-based models.

## License

This repo is for experimentation — add a license if you plan to publish.
