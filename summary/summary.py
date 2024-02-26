import streamlit as st
import webvtt, math
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from io import StringIO

st.set_page_config(page_title="Summarize",page_icon="📝")

st.title('📝 Teams meeting summarizer (powered by Mistral🌀)')

# Set the API key for the Mistral Python client
client = MistralClient(
    # defaults to os.environ.get("MISTRAL_API_KEY")?
    api_key=st.secrets['MISTRAL_API_KEY'],
)

chunk_size = 4000

def num_tokens(text: str) -> int:
    words = text.split() # split the string into words 
    num_tokens = math.floor(len(words) * 3/4) # 3/4 of the words are tokens
    return num_tokens

def slice_string(text: str) -> list[str]:
    # Split text into chunks based on space or newline
    chunks = text.split()

    # Initialize variables
    result = []
    current_chunk = ""

    # Concatenate chunks until the total length is less than 4096 tokens
    for chunk in chunks:
        # if len(current_chunk) + len(chunk) < 4096:
        if (len(current_chunk)+len(chunk)) < chunk_size * 3/4:
            current_chunk += " " + chunk if current_chunk else chunk
        else:
            result.append(current_chunk.strip())
            current_chunk = chunk
    if current_chunk:
        result.append(current_chunk.strip())

    return result

def summarize(context: str, model:str, convo: str) -> str:
    """Returns the summary of a text string."""
    context = context
    completion = client.chat(
    model = model,
        # messages=[
        #     {'role': 'system','content': context},
        #     {'role': 'user', 'content': convo}
        #         ]
        messages = [
            ChatMessage(role="system", content=context),
            ChatMessage(role="user", content=convo)
        ]
    )
    return completion.choices[0].message.content

context = st.text_input('Context','summarize the following conversation, with detailed bullet points')

model = st.radio('Model',('mistral-tiny', 'mistral-small','mistral-medium'))

maxtokens = {'mistral-tiny': 4000, 'mistral-small':32000, 'mistral-small':32000}
st.write(model,maxtokens[model],'tokens')
file = st.file_uploader('Upload Teams VTT transcript',type='vtt')

if file is not None:
    data = StringIO(file.getvalue().decode('utf-8'))
    chat = webvtt.read_buffer(data)
    # data = file.getvalue().decode('utf-8')
    # with open('vtt/'+file.name,'w') as f:
    #     f.write(data)
    # caption = webvtt.read('vtt/'+file.name)
    part = st.checkbox('include participants')
    time = st.checkbox('include time')
    str = []
    for caption in chat:
        if part & time:
            str.append(f'{caption.start} --> {caption.end}')
            str.append(caption.raw_text)
        elif time:
            str.append(f'{caption.start} --> {caption.end}')
            str.append(caption.text)
        elif part:
            str.append(caption.raw_text)
        else:
            str.append(caption.text)
    sep = '\n'
    convo = sep.join(str)
        
    convo = st.text_area('vtt file content',convo)
    toknum = num_tokens(convo)
    st.write(toknum,'tokens')
    if (toknum > maxtokens[model]):
        st.write(f'Text too long please prune to fit under {maxtokens[model]} tokens')
        bd = st.checkbox('Breakdown recording')
        if bd:
            chunks = slice_string(convo)
            sum = st.button('summarize')
        else:
            sum = st.button('summarize',disabled=True)
        if sum:
            for chunk in chunks:
                st.write(f'Summary of the meeting with {model}')
                st.write(summarize(context,model,chunk))
    else:
        sum = st.button('summarize')
    if sum & (toknum <= maxtokens[model]):
        st.write(f'Summary of the meeting with {model}')
        st.write(summarize(context,model,convo))

else:
    with open('vtt/YannMike_2023-03-08.vtt') as f:
        st.download_button(
            label="Sample VTT file",
            data=f,
            file_name="sample.vtt",
            mime="text/vtt"
          )