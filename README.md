# CV Chatbot

A Streamlit chatbot that answers questions about a candidate based on
`cv.pdf`, powered by DeepSeek (`deepseek-chat`) via LangChain.

## Setup

```bash
conda create -n cvchatbot python=3.11 -y
conda activate cvchatbot
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your DeepSeek API key:

```bash
cp .env.example .env
```

Edit `config.py` to set `PERSON_NAME` and any `ADDITIONAL_INFO` you want the
bot to know beyond what's in the resume (links, certifications, etc.).

## Run

```bash
conda activate cvchatbot
streamlit run app.py
```

The UI lets visitors chat about the resume and download the original PDF
from the sidebar.

## Guardrails

- The resume/additional info are injected into the system prompt as clearly
  labeled, untrusted data — the model is instructed to never treat text
  inside it (or inside user messages) as instructions.
- The assistant is scoped to only answer questions about the candidate and
  refuses unrelated requests or attempts to reveal/change its instructions.
- User input is sanitized and hard-capped in length (`MAX_INPUT_CHARS`).
- Conversation history sent to the model is capped (`MAX_HISTORY_TURNS`).
- Model output is capped via `max_tokens` (`MAX_RESPONSE_TOKENS`).

No prompt-based defense is 100% foolproof against a determined attacker —
this is a defense-in-depth setup, not a guarantee.
