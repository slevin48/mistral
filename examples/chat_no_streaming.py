from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os, tomli

with open('.streamlit/secrets.toml','rb') as f:
    secrets = tomli.load(f)
    
api_key = secrets["MISTRAL_API_KEY"]
# api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-tiny"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)