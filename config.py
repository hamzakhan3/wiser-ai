import os

# Local database (default)
LOCAL_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"

# AWS PostgreSQL database
AWS_DATABASE_URL = "postgresql+psycopg2://postgres:password@3.90.156.11:5432/postgres"

# Get database URL from environment variable, default to local
DATABASE_URL = os.getenv('DATABASE_URL', LOCAL_DATABASE_URL)

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "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")

print(f"🔗 Using Database URL: {DATABASE_URL}")
print(f"🔑 OpenAI API Key: {OPENAI_API_KEY[:20]}...{OPENAI_API_KEY[-10:]}")
