# from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
import streamlit as st

from utils.prompt_generator import prompt_generator
from utils.final_result_generator import final_result_generator
from utils.keyword_generator import keyword_generator
from utils.completion_checker import completion_checker



def is_first_chat(msg):
    return len(_cur_post_messages) == 1

st.title("2024-05-18 Upstage Project demo")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("질문을입력해주세요~"):
    print(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    print("user input - ", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        _cur_post_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        print("msg - ", len(_cur_post_messages), _cur_post_messages)
        if is_first_chat(_cur_post_messages):
            response = keyword_generator(_cur_post_messages)
        else:
            response = final_result_generator(_cur_post_messages)
        print("res - ", type(response), response)
        st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

