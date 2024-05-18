from . import client
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

def final_result_generator(messages_to_llm):
    """
    final_result_generator
    """
    print("final_result_generator")
    return client.chat.completions.create(
                model="solar-1-mini-chat",
                messages=messages_to_llm,
                stream=False,
        ).choices[0].message.content
    