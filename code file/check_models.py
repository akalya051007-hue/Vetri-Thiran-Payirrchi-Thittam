from app.ai.gemini_generator import get_gemini_client

client = get_gemini_client()

for model in client.models.list():
    print(model.name)