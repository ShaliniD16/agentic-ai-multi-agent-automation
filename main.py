import os

from openai import OpenAI
os.environ["GEMINI_API_KEY"] = "API key"

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

models = client.models.list()

for model in models:
    print(model.id)