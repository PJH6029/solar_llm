from langchain.schema import HumanMessage, AIMessage
def is_completed(histories, num_keywords):
    num_history = 0
    for hist in histories:
        if isinstance(hist, HumanMessage):
            num_history += 1
    return num_history >= num_keywords + 1