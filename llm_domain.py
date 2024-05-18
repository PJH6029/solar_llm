from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def keyword_generator(domain: str):
    query_template = """
    I need a list of keywords related to the domain of {domain}.
    These keywords should help in gathering detailed information necessary for completing a user's task in this domain.
    Please provide a comprehensive set of keywords that cover various aspects and details relevant to the task.
    For example, if the domain is 'writing a self-introduction document,' 
    the keywords could include name, age, background, skills, hobbies, achievements, goals, etc. 
    Make sure the keywords are specific and cover a broad range of relevant details.
    List all keywords with the following format:
    1. Name
    2. Age
    3. Background
    ...etc.
    
    You don't need to provide additional explanations or details for each keyword.
    You just list the keywords in a clear and concise manner.
    """

    prompt = ChatPromptTemplate.from_template(query_template)

    generate_keywords = (
        prompt
        | ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY"))
        | StrOutputParser()
    )

    return (generate_keywords.invoke({"domain": domain}))

if __name__ == "__main__":
    load_dotenv()
    result = keyword_generator("writing a self-introduction document")
    print(result)