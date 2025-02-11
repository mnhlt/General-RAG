from rag_agent import app

def test_rag_agent():
    final_state = app.invoke(
        {"messages": [{"role": "user", "content": "What is LangGraph?"}]}
    )
    assert "LangGraph" in final_state["messages"][-1].content 