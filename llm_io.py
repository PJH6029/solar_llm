from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
import streamlit as st
import gradio as gr

from llm_domain import keyword_generator

st.title("Langchain Chat Demo")

load_dotenv()
llm = ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY"), streaming=True)

system_prompt_template = """
I have a list of keywords related to a specific domain, 
and I need you to generate a series of questions to gather detailed information for completing a task in that domain. 
Based on the following keywords, please create specific and user-friendly questions that will help in collecting the necessary information:

{keywords}

For example, if the keywords are related to writing a self-introduction document, 
such as name, age, background, skills, hobbies, achievements, goals, etc., 
you should generate questions like:

What is your name?
How old are you?
Can you provide a brief background about yourself?
What are your key skills?
What hobbies do you enjoy?
What achievements are you most proud of?
What are your goals for the future?

Make sure the questions are clear, concise, and cover all the relevant aspects of the task. 
Provide one question for each keyword.
You should ask questions one by one, not all at once.
"""

chat_with_history_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{message}"),
    ]
)

chain = chat_with_history_prompt | llm | StrOutputParser()
domain = "writing a self-introduction document"
keywords = keyword_generator(domain)
print(keywords)

def chat(message, history, keywords=keywords):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    generator = chain.stream({"message": message, "history": history_langchain_format, "keywords": keywords})

    assistant = ""
    for gen in generator:
        assistant += gen
        yield assistant

with gr.Blocks() as demo:
    chatbot = gr.ChatInterface(
        chat,
        examples=[],
        title="Chat with Langchain",
        description="This is a chat interface that uses Langchain to generate questions based on a list of keywords.",
    )
    chatbot.chatbot.height = 300

if __name__ == "__main__":
    demo.launch()