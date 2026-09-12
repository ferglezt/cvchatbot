import os

import streamlit as st
from dotenv import load_dotenv

import config
import usage_tracker
from chatbot import ChatbotError, get_response, load_resume_text

load_dotenv()

st.set_page_config(page_title=f"Chat about {config.PERSON_NAME}", page_icon="\U0001F4C4")


@st.cache_data(show_spinner=False)
def _load_resume_text_cached(cv_mtime):
    return load_resume_text(config.CV_PATH)


@st.cache_data(show_spinner=False)
def _load_cv_bytes(cv_mtime):
    with open(config.CV_PATH, "rb") as f:
        return f.read()


def _cv_mtime():
    return os.path.getmtime(config.CV_PATH)


def _linkify_pets(text):
    return text.replace(
        config.PETS_TRIGGER_PHRASE,
        f"[{config.PETS_TRIGGER_PHRASE}](?show_pets=1)",
    )


st.title(f"Ask about {config.PERSON_NAME}")
st.caption(
    f"This assistant answers questions about {config.PERSON_NAME}'s professional background. "
    "It won't help with unrelated tasks."
)

with st.sidebar:
    st.header("Resume")
    try:
        cv_bytes = _load_cv_bytes(_cv_mtime())
        st.download_button(
            label="Download CV (PDF)",
            data=cv_bytes,
            file_name=config.CV_PATH,
            mime="application/pdf",
        )
    except FileNotFoundError:
        st.error(f"CV file not found: {config.CV_PATH}")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    with st.expander("About this site"):
        st.markdown(
            f"""
Built by **{config.PERSON_NAME}** — the person this chatbot answers
questions about — as a way to explore his resume interactively.

**Stack:**
- [Streamlit](https://streamlit.io) — web UI
- [LangChain](https://www.langchain.com) — LLM orchestration
- [DeepSeek](https://www.deepseek.com) (`deepseek-chat`) — language model
- [pypdf](https://pypdf.readthedocs.io) — resume text extraction
"""
        )

try:
    resume_text = _load_resume_text_cached(_cv_mtime())
except ChatbotError as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.query_params.get("show_pets"):
    st.session_state.messages.append(("image", config.PETS_IMAGE_PATH))
    st.query_params.clear()
    st.rerun()

for role, content in st.session_state.messages:
    if role == "image":
        with st.chat_message("assistant"):
            st.image(content, caption=config.PETS_TRIGGER_PHRASE)
    else:
        with st.chat_message(role):
            st.markdown(_linkify_pets(content) if role == "assistant" else content)

if config.SUGGESTED_QUESTIONS:
    st.caption("Try asking:")
    cols = st.columns(len(config.SUGGESTED_QUESTIONS))
    clicked_question = None
    for col, suggestion in zip(cols, config.SUGGESTED_QUESTIONS):
        if col.button(suggestion, type="tertiary", use_container_width=True):
            clicked_question = suggestion
else:
    clicked_question = None

typed_question = st.chat_input(
    f"Ask a question about {config.PERSON_NAME}'s background...",
    max_chars=config.MAX_INPUT_CHARS,
)

question = clicked_question or typed_question

if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append(("user", question))

    with st.chat_message("assistant"):
        client_id = st.context.ip_address or "unknown"
        tokens_used = 0

        if usage_tracker.is_over_limit(client_id):
            answer = (
                "This chatbot has a daily usage limit to keep API costs in check, "
                "and your network has reached it for today. Please try again tomorrow."
            )
            st.warning(answer)
        else:
            with st.spinner("Thinking..."):
                try:
                    answer, tokens_used = get_response(
                        question=question,
                        history=st.session_state.messages[:-1],
                        resume_text=resume_text,
                    )
                except ChatbotError as e:
                    answer = f"Configuration error: {e}"
                except Exception as e:
                    answer = f"Sorry, something went wrong while contacting the model: {e}"
            st.markdown(_linkify_pets(answer))

        if tokens_used:
            usage_tracker.add_usage(client_id, tokens_used)

        combined_text = f"{question} {answer}".lower()
        if any(keyword in combined_text for keyword in config.DOWNLOAD_KEYWORDS):
            try:
                st.download_button(
                    label=f"Download {config.PERSON_NAME}'s CV (PDF)",
                    data=_load_cv_bytes(_cv_mtime()),
                    file_name=config.CV_PATH,
                    mime="application/pdf",
                    key=f"inline_download_{len(st.session_state.messages)}",
                )
            except FileNotFoundError:
                pass
    st.session_state.messages.append(("assistant", answer))
