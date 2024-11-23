#%%
from mistralai import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

model = "mistral-tiny"
client = Mistral(api_key=api_key)

m = [{'role': 'system', 'content': 'If I say hello, say world'},
     {'role': 'user', 'content': 'hello'}]
chat_response = client.chat.complete(
    model = model,
    messages = m
)

print(chat_response.choices[0].message.content)
# %%
