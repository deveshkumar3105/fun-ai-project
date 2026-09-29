# fun-ai-project

Small playground for experimenting with LangChain, Google Generative AI, and Streamlit-based demos..

## Structure

- `apps/` — small Streamlit apps (chatbots, demos).
- `notebooks/` — Jupyter notebooks with examples and exploratory code.
- `requirements.txt` — Python dependencies.

## Setup

1. Create a Python virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your secrets in a `.env` file (do NOT commit it):

```
GOOGLE_API_KEY=your_api_key_here
OTHER_SECRET=...
```

4. Run the Streamlit demo:

```bash
streamlit run apps/1_qna_chatbot.py
```

## Notes

- `.env` is listed in `.gitignore` to avoid accidentally committing credentials.
- Replace model names and API keys as needed for your account.

## License

This repo is for experimentation — add a license if you plan to publish.
