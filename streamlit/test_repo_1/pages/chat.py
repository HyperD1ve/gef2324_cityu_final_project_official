import streamlit as st
from menu import menu
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../private')))
# from keys import * #never mind the warning, this code works. the sys code is to join the private folder to this directory in order to fetch the keys.py file. 

# Authenticate with Hugging Face Hub
from huggingface_hub import login
HUGGING_FACE_KEY = "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"
login(HUGGING_FACE_KEY)  # Replace with your token if not already logged in

menu()

st.title("Chat with our bot")

#initialise the session variable messages so that they are not lost upon reload
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello, I am DSEBot"})


#display messages after reload 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Load the Llama 2 model
model_name = "meta-llama/Llama-3.2-3B"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGING_FACE_KEY)
model = AutoModelForCausalLM.from_pretrained(model_name, token=HUGGING_FACE_KEY)

# Set up the pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
def Chat(msg):
    output = pipe(str(msg))
    print(output)
    try:
        res = output[0]['generated_text']
        for word in res.split():
            yield word + " "
            time.sleep(0.01)
    except (KeyError, TypeError) as e:
        print(f"Error accessing generated text: {e}")

#chatbox and appending to messages
if prompt := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
     
    with st.chat_message("assistant"):
        response = st.write_stream(Chat(prompt)) 
    st.session_state.messages.append({"role": "assistant", "content": response}) 
    
