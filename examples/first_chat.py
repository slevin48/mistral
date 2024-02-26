from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import streamlit as st
client = MistralClient(
    # defaults to os.environ.get("MISTRAL_API_KEY")?
    api_key=st.secrets['MISTRAL_API_KEY'],
)
model = "mistral-tiny"
st.title('My first chatbot 🤖')
# m = [{'role': 'system', 'content': 'If I say hello, say world'}]
messages = [ChatMessage(role='system', content='If I say hello, say world')]

prompt = st.text_input('Enter your message')
if prompt:
    # m.append({'role': 'user', 'content': prompt})
    messages.append(ChatMessage(role='user', content=prompt))
    completion = client.chat(model=model, messages=messages)
    response = completion.choices[0].message.content
    st.write(response)