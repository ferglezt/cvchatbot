"""
Editable configuration for the CV chatbot.

Fill in PERSON_NAME and ADDITIONAL_INFO below with anything that isn't
already in cv.pdf but that you'd like the chatbot to know about (links,
certifications, availability, preferred contact method, a short personal
statement, etc.). This text is treated as trusted background context,
exactly like the resume itself.
"""

PERSON_NAME = "Fernando González"  # shown in the UI title

# Free-form text. Add as many lines/paragraphs as you like.
ADDITIONAL_INFO = """
- GitHub: https://github.com/ferglezt
- LinkedIn: https://www.linkedin.com/in/fernando-gonz%C3%A1lez-b4a9ba124/
- Portfolio / personal site: (add link)
- Certifications not listed on the resume: (add here)
- Location: Mexico City
- Languages: Spanish (native), English C2 (fluent)
- Availability / open to relocation: (add here)
- Preferred contact method: (add here)
- Hobbies / interests: BJJ, Soccer goalkeeping, Science fiction, Poker, Chess
""".strip()

# --- Guardrails / limits (tune if needed) ---
MAX_RESPONSE_TOKENS = 600      # cap on tokens generated per reply
MAX_INPUT_CHARS = 1500          # cap on a single user question's length
MAX_HISTORY_TURNS = 5           # how many past exchanges to keep in context
MAX_RESUME_CHARS = 20000        # safety cap on extracted resume text length

CV_PATH = "cv.pdf"

# Shown as quick-click suggestions above the chat input.
SUGGESTED_QUESTIONS = [
    "What are his main Android skills?",
    "What's his current role?",
    "What's his most recent experience?",
    "How can I contact him?",
]
