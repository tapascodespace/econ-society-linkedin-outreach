"""Configuration for the Economics Society LinkedIn outreach system."""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")

CLAUDE_MODEL = "claude-3-5-sonnet-20240620"

# LinkedIn daily limits
MAX_CONNECTION_REQUESTS_PER_DAY = 22
MAX_MESSAGES_PER_DAY = 50
MAX_PROFILE_VIEWS_PER_DAY = 120

# Outreach segments
SEGMENTS = {
    "professor": {
        "tone": "professional, academic",
        "focus": "guest lectures, research collaboration, academic partnerships",
        "sequence_days": [0, 3, 7, 14],
    },
    "alumni": {
        "tone": "warm, community-oriented",
        "focus": "mentorship, networking events, career panels",
        "sequence_days": [0, 2, 5, 10],
    },
    "professional": {
        "tone": "professional but approachable",
        "focus": "speaker events, sponsorship, internship pipelines",
        "sequence_days": [0, 3, 7, 14, 21],
    },
    "student": {
        "tone": "casual, peer-to-peer",
        "focus": "society membership, event attendance, study groups",
        "sequence_days": [0, 2, 5],
    },
}

# Society details used in message generation
SOCIETY_NAME = "University Economics Society"
SOCIETY_LINKEDIN_URL = "https://www.linkedin.com/company/uni-econ-society"
SOCIETY_DESCRIPTION = (
    "A student-run society dedicated to bridging academic economics "
    "with real-world applications through speaker events, workshops, "
    "and networking opportunities."
)
