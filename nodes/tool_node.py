# ---------------------------------------------------------
# Tool Node 1
# ---------------------------------------------------------

from langgraph.prebuilt import ToolNode


def tool_node1(state, llm, tools):
    """
    사용자 메시지를 분석하여 필요한 툴을 호출하는 노드입니다.
    LLM에 툴을 바인딩하고, 사용자 메시지를 기반으로 툴 호출을 생성합니다.

    Args:
        state: 현재 State 객체 (messages, contents_word 필드를 포함)
        llm: LLM 인스턴스 (llm1)
        tools: 사용 가능한 툴 리스트

    Returns:
        dict: 업데이트된 State (answer_word 필드 추가)
    """
    messages = state["messages"][-1].content
    contents_word = state.get("contents_word", "")

    user_query = f"""
    사용할 수 있는 툴만 사용하세요.
    {messages}

    내용 : {contents_word}
    """

    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(user_query)

    print(f"툴 호출 메세지 : {response}")
    tool_node = ToolNode(tools)
    result = tool_node.invoke({"messages": [response]})
    print(f"user_query : {user_query}")
    
    return {"answer_word": result}

