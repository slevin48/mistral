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
    # With streaming
    stream_response = client.chat_stream(model=model, messages=messages)
    report = []
    res_box = st.empty()
    # Looping over the response
    for resp in stream_response:
        if resp.choices[0].finish_reason is None:
            # join method to concatenate the elements of the list 
            # into a single string, then strip out any empty strings
            report.append(resp.choices[0].delta.content)
            result = ''.join(report).strip()
            result = result.replace('\n', '')        
            res_box.write(result) 