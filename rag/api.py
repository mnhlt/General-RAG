from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import json
from rag_agent import app as rag_agent, Message, streaming_app
from knowledge_base import ChromaDBKnowledgeBase
from llm_wrapper import OpenAIAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["Content-Type", "Authorization"]
)

class Query(BaseModel):
    message: str
    thread_id: str = "default"

@app.post("/query")
async def query(query: Query):
    try:
        logger.info(f"Received query: {query.message}")
        initial_message: Message = {"role": "user", "content": query.message}
        final_state = rag_agent.invoke(
            {"messages": [initial_message], "stream": False},
            config={"configurable": {"thread_id": query.thread_id}}
        )
        logger.info(f"Final state: {final_state}")
        return {"response": final_state["messages"][-1]["content"]}
    except Exception as e:
        logger.error(f"Error in query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query-stream")
async def query_stream(query: Query):
    try:
        logger.info(f"Received streaming query: {query.message}")
        initial_message: Message = {"role": "user", "content": query.message}
        
        async def generate():
            try:
                response = streaming_app.invoke(
                    {"messages": [initial_message], "stream": True},
                    config={"configurable": {"thread_id": query.thread_id}}
                )
                messages = response.get("messages", [])
                if not messages:
                    error_msg = json.dumps({"error": "No messages in response"})
                    yield f"event: error\ndata: {error_msg}\n\n"
                    yield f"event: done\ndata: [DONE]\n\n"
                    return

                for i, message in enumerate(messages):
                    if message["role"] == "assistant":
                        yield f"id: {i}\nevent: message\ndata: {json.dumps({'content': message['content']})}\n\n"
                yield f"event: done\ndata: [DONE]\n\n"
            except Exception as e:
                error_msg = json.dumps({"error": str(e)})
                yield f"event: error\ndata: {error_msg}\n\n"
                yield f"event: done\ndata: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in streaming query endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.options("/query-stream")
async def query_stream_options():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@app.options("/query")
async def query_options():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@app.post("/update")
async def update(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}")
        kb = ChromaDBKnowledgeBase()
        content = await file.read()
        
        if file.filename.endswith(".txt"):
            # Read plain text
            text_content = content.decode('utf-8')
            logger.info(f"Text content: {text_content[:100]}...")
            kb.add_documents([text_content])
            return {"message": "Knowledge base updated successfully with text content"}
            
        elif file.filename.endswith(".json"):
            # Parse JSON content
            try:
                json_data = json.loads(content.decode('utf-8'))
                
                # Handle our crawler's JSON format
                if isinstance(json_data, dict) and 'content' in json_data:
                    text_content = json_data['content']
                    source_url = json_data.get('url', 'Unknown source')
                    timestamp = json_data.get('timestamp', 'Unknown time')
                    
                    logger.info(f"Processing JSON from {source_url} at {timestamp}")
                    logger.info(f"Content preview: {text_content[:100]}...")
                    
                    kb.add_documents([text_content])
                    return {
                        "message": "Knowledge base updated successfully with JSON content",
                        "source": source_url,
                        "timestamp": timestamp
                    }
                else:
                    # Handle array of text or other JSON formats
                    if isinstance(json_data, list):
                        text_content = [str(item) for item in json_data]
                    else:
                        text_content = [json.dumps(json_data, ensure_ascii=False)]
                    
                    kb.add_documents(text_content)
                    return {"message": "Knowledge base updated successfully with JSON content"}
                    
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
                
        elif file.filename.endswith(".pdf"):
            # Extract text from PDF
            return {"message": "PDF support coming soon"}
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
    except Exception as e:
        logger.error(f"Error in update endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 