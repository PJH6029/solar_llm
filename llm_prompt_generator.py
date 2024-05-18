from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def prompt_generator(domain, histories):
    question_ans = [("제가 어떤 일을 도와드릴 수 있나요?", domain)]
    for i in range(0, len(histories), 2):
        question = histories[i]
        answer = histories[i+1]
        question_ans.append((question, answer))
    print(question_ans)

    prompt_template = """
    사용자 작업과 관련된 일련의 질문-답변 쌍이 있습니다. 
    제공된 정보를 기반으로 사용자에게 작업을 완료하도록 요청하는 포괄적인 프롬프트를 생성해야 합니다. 
    답변을 사용하여 일관되고 자세한 프롬프트를 만드세요. 질문-답변 쌍의 예시는 다음과 같습니다.
    첫 번째 질문은 "제가 어떤 일을 도와드릴 수 있나요?"이며, 사용자의 작업이 무엇인지 설명합니다.

    질문-답변 쌍 예시:
    [
    ("제가 어떤 일을 도와드릴 수 있나요?", "자기 소개서 작성을 도와주세요"),
    ("몇 살이세요?", "24살입니다"),
    ("어디서 오셨어요?", "한국"),
    ("당신의 직업은 무엇입니까?", "소프트웨어 엔지니어"),
    ("취미는 무엇입니까?", "독서와 하이킹"),
    ("당신의 전문 기술은 무엇입니까?", "Python, Java, Machine Learning"),
    ("당신의 경력 목표는 무엇입니까?", "최고의 AI 연구자가 되는 것"),
    ("중요한 성과를 설명해주실 수 있나요?", "매출이 20% 증가한 AI 모델 개발"),
    ("당신의 교육 자격은 무엇입니까?", "컴퓨터 과학 학사 학위")
    ]
    
    위의 데이터는 예시일 뿐이며, 실제로 주어진 질문 답변 쌍은 다음과 같습니다.
    
    {question_ans}

    이러한 쌍을 사용하여 사용자의 작업을 완료하는 데 사용할 수 있는 프롬프트를 생성합니다.
    사용자의 작업은 질문-답변 쌍의 첫 번째 질문에서 확인할 수 있습니다.
    프롬프트는 자세해야 하며 제공된 답변을 효과적으로 활용해야 합니다.
    
    예를 들어, 다음과 같은 프롬프트를 생성할 수 있습니다.
    
    프롬프트 예시:
    아래 정보를 활용하여 자기소개서를 작성해주세요. 
    포괄적이고 매력적인 소개를 작성하려면 모든 세부 정보를 포함해야 합니다.

    이름: [당신의 이름]
    나이: 24세
    보낸 사람: 한국
    직위: 소프트웨어 엔지니어
    취미: 독서와 하이킹
    전문 기술: Python, Java, 기계 학습
    진로목표 : 선도적인 AI 연구자가 되는 것
    의의 있는 성과: 매출 20% 증가 AI 모델 개발
    교육 자격: 컴퓨터 공학 학사 학위
    이 정보를 활용하여 다재다능하고 상세한 자기소개서를 작성하세요. 
    간략한 소개로 시작하고 배경, 전문적 경험, 기술, 취미, 성취 및 직업 포부에 대한 섹션이 이어집니다.
    귀하의 강점과 귀하를 특별하게 만드는 요소를 강조하십시오.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    generate_prompt = (
        prompt
        | ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY"))
        | StrOutputParser()
    )

    return (generate_prompt.invoke({"question_ans": str(question_ans)}))