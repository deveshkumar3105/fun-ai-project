from dotenv import load_dotenv

# Load environment variables from a `.env` file (e.g. API keys, project IDs).
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

# Instantiate the Google Generative AI LLM wrapper from LangChain.
# Model name can be changed to another available Gemini model.
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

# Streamlit UI: page title and short description shown at the top.
st.title("Q&A Chatbot 👋🏼")
st.markdown(
    """
This is a simple Q&A chatbot built using LangChain and Google Generative AI.
"""
)

# Input widget for user queries. This returns the submitted string when the user
# presses Enter or the send button.
query = st.chat_input("Ask me anything...")

# Use Streamlit session state to persist the chat history across reruns.
if "messages" not in st.session_state:
    # Each entry is a dict: {"role": "user"|"ai", "content": str}
    st.session_state.messages = []

# Render previous messages from the session (if any).
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    # `st.chat_message(role)` creates a chat bubble for the given role.
    st.chat_message(role).markdown(content)

# When the user submits a query, append it to the session, display it, call the LLM,
# and append the model response back into the session state.
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)

    # Call the LLM. `invoke` returns a response object; adjust handling if your
    # LangChain wrapper returns a different structure.
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content[0]['text'])
    st.session_state.messages.append({"role": "ai", "content": res.content[0]['text']})