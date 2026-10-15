import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_APP_NAME = "FitBuddy - AI Fitness Plan Generator"


# -----------------------------
# Gemini Configuration
# -----------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

# -----------------------------
# Database Configuration
# -----------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)


# -----------------------------
# Admin Configuration
# -----------------------------

ADMIN_KEY = os.getenv(
    "ADMIN_KEY",
    "fitbuddy-admin"
)