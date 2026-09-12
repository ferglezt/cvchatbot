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
- Hobbies / interests: BJJ, MMA, Soccer goalkeeping, Science fiction, Anime, Learning Japanese, Poker, Chess, Spoil his cats Chucky and Chango
""".strip()

# --- Guardrails / limits (tune if needed) ---
MAX_RESPONSE_TOKENS = 600      # cap on tokens generated per reply
MAX_INPUT_CHARS = 1500          # cap on a single user question's length
MAX_HISTORY_TURNS = 5           # how many past exchanges to keep in context
MAX_RESUME_CHARS = 20000        # safety cap on extracted resume text length
MAX_TOKENS_PER_IP_PER_DAY = 100_000  # daily token budget per client IP
USAGE_STORE_PATH = "usage_data.json"  # local file tracking daily usage per IP

CV_PATH = "cv.pdf"

# Shown as quick-click suggestions above the chat input.
SUGGESTED_QUESTIONS = [
    "What are his main Android skills?",
    "What's his current role?",
    "What's his most recent experience?",
    "What are his hobbies?",
    "How can I contact him?",
]

# When this phrase appears in a chat message, it's turned into a link that
# reveals the photo below in the chat.
PETS_TRIGGER_PHRASE = "Chucky and Chango"
PETS_IMAGE_PATH = "chuckychango.jpg"

# Background info about the site itself, so the bot can answer meta questions
# ("what is this?", "who built this?", "can I get the PDF?").
SITE_INFO = f"""
This chatbot is a website that lets visitors ask questions about {PERSON_NAME}'s
resume. It was built by {PERSON_NAME} himself, the same person the resume
belongs to. It's built with:
- Streamlit for the web interface
- LangChain for orchestrating the conversation with the language model
- DeepSeek's deepseek-chat model for answering questions
- pypdf for extracting text from the resume PDF
Visitors can download the original resume PDF at any time using the download
button in the sidebar, or by asking this assistant for it.
""".strip()

# Keywords that trigger an inline "download the CV" button in the chat.
DOWNLOAD_KEYWORDS = ["download", "pdf", ".pdf", "resume file", "cv file", "get his cv", "get his resume"]
