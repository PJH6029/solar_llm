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
특정 도메인과 관련된 키워드 목록이 있는데,
그리고 해당 영역의 작업을 완료하기 위한 자세한 정보를 수집하려면 일련의 질문을 생성해야 합니다.
다음 키워드를 기반으로 필요한 정보를 수집하는 데 도움이 될 구체적이고 사용자 친화적인 질문을 작성하십시오.

{keywords}

예를 들어 자기소개서 작성과 관련된 키워드가 있다면,
이름, 나이, 배경, 기술, 취미, 업적, 목표 등
다음과 같은 질문을 생성해야 합니다.

이름이 뭐에요?
몇 살이에요?
자신에 대한 간략한 배경을 제공해 주실 수 있나요?
당신의 핵심 기술은 무엇입니까?
어떤 취미를 즐기시나요?
당신이 가장 자랑스러워하는 성과는 무엇입니까?
미래에 대한 당신의 목표는 무엇입니까?

질문이 명확하고 간결하며 작업과 관련된 모든 측면을 포괄하는지 확인하세요.
각 키워드에 대해 하나의 질문을 제공하십시오.
한꺼번에 질문하지 말고 하나씩 질문해야 합니다.

질문에 대한 답변을 받은 이후에는,
알맞게 이해했는지 확인하기 위해 답변을 되풀이해주십시오.
예를 들어,
Q. 이름이 뭐에요?
A. 제 이름은 홍길동입니다.
Q. 이름이 홍길동이시군요, 다음 질문입니다. 몇 살이신가요?
와 같이 되풀이해주십시오.
"""

chat_with_history_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{message}"),
    ]
)

chain = chat_with_history_prompt | llm | StrOutputParser()
domain = "내가 가르치는 학생의 생활기록부를 작성하고 싶어"
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