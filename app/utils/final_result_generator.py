from . import client

def final_result_generator(messages_to_llm):
    """
    final_result_generator
    """
    print("final_result_generator")
    return client.chat.completions.create(
            model="solar-1-mini-chat",
            messages=messages_to_llm,
            stream=True,
        )
    