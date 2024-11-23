from mistralai import Mistral
import json, os
import streamlit as st

st.set_page_config(page_title='Mistral Chat',page_icon='🤖')

avatar = {"assistant": "🤖", "user": "🌀"}
model = "mistral-tiny"

# Set the API key for the Mistral Python client
client = Mistral(
    # defaults to os.environ.get("MISTRAL_API_KEY")?
    api_key=st.secrets['MISTRAL_API_KEY'],
)

# Functions
def new_chat():
   st.session_state.convo = []
   st.session_state.id += 1

def save_chat(n):
  file_path = f'chat/convo{n}.json'
  with open(file_path,'w') as f:
    json.dump(st.session_state.convo, f, indent=4)

def select_chat(file):
  st.session_state.convo = []
  with open(f'chat/{file}') as f:
    st.session_state.convo = json.load(f)
  st.session_state.id = int(file.replace('.json','').replace('convo',''))

def dumb_chat():
  with open('fake/dummy1.json') as f:
    dummy = json.load(f)
  st.write(dummy[1]['content'])
  return dummy[1]['content']

def chat_stream(messages,model='mistral-tiny'):
  # Generate a response from the large language model
  stream_response = client.chat.stream(model=model, messages=messages)
  report = []
  res_box = st.empty()
  # Looping over the response
  for resp in stream_response:
      if resp.data.choices[0].finish_reason is None:
          # join method to concatenate the elements of the list 
          # into a single string, then strip out any empty strings
          report.append(resp.data.choices[0].delta.content)
          result = ''.join(report).strip()
          result = result.replace('\n', '')        
          res_box.write(result) 
  return result


# Initialization
if 'convo' not in st.session_state:
    st.session_state.convo = []

n = len(os.listdir('chat'))
if 'id' not in st.session_state:
    st.session_state.id = n+1

id = st.session_state.id

st.sidebar.title('ChatGPT-like bot 🤖')

# Debug
# st.sidebar.write(st.session_state.convo)

if st.sidebar.button('New Chat 🌀'):
   new_chat()
for file in sorted(os.listdir('chat')):
  filename = file.replace('.json','')
  if st.sidebar.button(f'💬 {filename}'):
     select_chat(file)

# Display the response in the Streamlit app
for line in st.session_state.convo:
    # st.chat_message(line.role,avatar=avatar[line.role]).write(line.content)
    if line['role'] == 'user':
      st.chat_message('user',avatar=avatar['user']).write(line['content'])
    elif line['role'] == 'assistant':
      st.chat_message('assistant',avatar=avatar['assistant']).write(line['content'])

# Create a text input widget in the Streamlit app
prompt = st.chat_input(f'convo{st.session_state.id}')

if prompt:
  # Append the text input to the conversation
  with st.chat_message('user',avatar='🌀'):
    st.write(prompt)
  st.session_state.convo.append({'role':'user', 'content':prompt})
  # Query the chatbot with the complete conversation
  with st.chat_message('assistant',avatar='🤖'):
     result = chat_stream(st.session_state.convo)
    #  result = dumb_chat()
  # Add response to the conversation
  st.session_state.convo.append({'role':'assistant','content':result})
  save_chat(id)

# # Write the chat log to a json file
# if st.sidebar.button('Save chat 🌀🤖'):
#   save_chat(id)