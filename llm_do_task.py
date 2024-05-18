from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def do(prompt):
    prompt_template = ChatPromptTemplate.from_template(prompt)
    chain = prompt_template | ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY")) | StrOutputParser()
    return chain.invoke({})