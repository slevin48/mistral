#%%
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

model = "mistral-tiny"
client = MistralClient(api_key=api_key)

m = [{'role': 'system', 'content': 'If I say hello, say world'}]

def struct2chat(struct):
    return [ChatMessage(role=m['role'], content=m['content']) for m in struct]

struct2chat(m) # [ChatMessage(role='system', content='If I say hello, say world')]

#%%
messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

def chat2struct(chat):
    return [{'role': m.role, 'content': m.content} for m in chat]

chat2struct(messages) # [{'role': 'user', 'content': 'What is the best French cheese?'}]

#%%
# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)
