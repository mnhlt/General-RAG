from typing import TypedDict, List, Union, Dict, Any, Generator
import logging
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from llm_wrapper import OpenAIAdapter
from knowledge_base import ChromaDBKnowledgeBase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Message(TypedDict):
    role: str
    content: str

class AgentState(TypedDict):
    messages: List[Message]
    context: Union[str, None]
    stream: bool

def retriever_node(state: AgentState) -> Dict[str, Any]:
    logger.info(f"Retriever input state: {state}")
    query = state['messages'][-1]['content']
    kb = ChromaDBKnowledgeBase()
    docs = kb.get_documents(query)
    context = " ".join(docs)
    logger.info(f"Retrieved context: {context}")
    return {"context": context}

def generator_node(state: AgentState) -> Dict[str, Any]:
    logger.info(f"Generator input state: {state}")
    messages = state['messages'].copy()
    context = state.get('context', '')
    stream = state.get('stream', False)
    
    # Add context as a system message
    system_message = {"role": "system", "content": f"Use this context to answer the question: {context}"}
    messages = [system_message] + messages
    logger.info(f"Messages to LLM: {messages}")
    
    model = os.environ.get("LLM_MODEL", "deepseek-r1-distill-llama-8b")  # Default if not set
    
    # Print environment variables for debugging
    logger.info("Environment variables:")
    for key, value in os.environ.items():
        logger.info(f"{key}: {value}")

    llm = OpenAIAdapter(
        api_key=os.environ["LLM_API_KEY"],
        base_url=os.environ["LLM_BASE_URL"],
        model=model
    )
    
    if stream:
        # Return each chunk as a message
        return {"messages": [{"role": "assistant", "content": chunk} for chunk in llm.generate(messages, stream=True)]}
    
    response = llm.generate(messages)
    logger.info(f"LLM response: {response}")
    return {"messages": [{"role": "assistant", "content": response}]}

# Regular workflow
workflow = StateGraph(AgentState)
workflow.add_node("retriever", retriever_node)
workflow.add_node("generator", generator_node)

# Add edge from START to retriever
workflow.add_edge(START, "retriever")
# Add edge from retriever to generator
workflow.add_edge("retriever", "generator")

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Streaming workflow
streaming_workflow = StateGraph(AgentState)
streaming_workflow.add_node("retriever", retriever_node)
streaming_workflow.add_node("generator", generator_node)

streaming_workflow.add_edge(START, "retriever")
streaming_workflow.add_edge("retriever", "generator")

streaming_app = streaming_workflow.compile(checkpointer=checkpointer) 