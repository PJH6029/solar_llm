# from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
import streamlit as st

from utils.prompt_generator import prompt_generator
from utils.final_result_generator import final_result_generator
from utils.keyword_generator import keyword_generator
from utils.completion_checker import completion_checker


st.title("2024-05-18 Upstage Project demo")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

palceholder = "질문을입력해주세요~"

import random

if prompt := st.chat_input( palceholder[0:random.randint(0, len(palceholder)-1)] ):
    st.session_state.messages.append({"role": "user", "content": prompt})
    print("user input - ", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        _cur_post_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        print("msg - ", _cur_post_messages)
        stream = final_result_generator(_cur_post_messages)
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})