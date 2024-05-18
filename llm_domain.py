from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def keyword_generator(domain: str, num_keywords=10):
    query_template = """
    {domain} 라는 임무를 수행하기 위한 키워드 목록이 필요합니다.
    우리는 이 키워드 목록을 이용해 추후에 사용자에게 질문을 생성할 것입니다.
    그리고 질문에 대한 답변을 바탕으로, LLM에게 임무를 맡기기 위한 prompt를 작성할 것입니다.
    따라서, 사용자에게 질문할 목록을 만들기 위한 키워드 목록을 제공해 주십시오.
    이러한 키워드는 이 도메인에서 사용자 작업을 완료하는 데 필요한 자세한 정보를 수집하는 데 도움이 됩니다.
    작업과 관련된 다양한 측면과 세부 사항을 포괄하는 포괄적인 키워드 집합를 제공하세요.
    예를 들어 '자기소개서 작성'이라는 도메인이 있다면,
    키워드에는 이름, 나이, 배경, 기술, 취미, 업적, 목표 등이 포함될 수 있습니다.
    키워드가 구체적이고 광범위한 관련 세부정보를 포함하는지 확인하세요.
    다음 형식으로 {num}개 이하의 키워드를 나열하십시오. 가장 중요한 키워드만 선택하여 나열해주십시오.
    1. 이름
    2. 나이
    3. 배경
    ...등.
    
    각 키워드에 대해 추가 설명이나 세부정보를 제공할 필요는 없습니다.
    명확하고 간결하게 {num}개 이하의 키워드를 나열하면 됩니다.
    """

    prompt = ChatPromptTemplate.from_template(query_template)

    generate_keywords = (
        prompt
        | ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY"))
        | StrOutputParser()
    )

    return (generate_keywords.invoke({"domain": domain, "num": num_keywords}))

if __name__ == "__main__":
    load_dotenv()
    result = keyword_generator("writing a self-introduction document", num_keywords=3)
    print(result)