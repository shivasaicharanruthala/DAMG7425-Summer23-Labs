import fastapi
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from starlette.responses import JSONResponse

app = FastAPI(title="DAMG7245 Lab")


class UserInput(BaseModel):
    service: str
    apikey: str
    content: list


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


@app.get('/api/v1/health')
async def healthcheck() -> dict:
    return {"message": "Ok"}


@app.post("/api/v1/tokenize")
async def tokenize(userinput: UserInput) -> JSONResponse:
    # user input validations

    # service validation
    if userinput.service not in ["huggingface", "openai", "cohere"]:
        raise HTTPException(status_code=404, detail=r"Service not among 'huggingface', 'openai', 'cohere'")

    # content validation
    print(len(userinput.content))
    if len(userinput.content) < 1:
        raise HTTPException(status_code=404, detail=r"Content should be a list of one or more than items")

    response = {"userinput": userinput.content}
    # tokenization
    if userinput.service == "huggingface":
        embeddings = model.encode(userinput.content)
        response["embeddings"] = embeddings.tolist()
        return JSONResponse(content=response)
    elif userinput.service == "openai":
        # Call OpenAI API
        return JSONResponse(content="OK")
    elif userinput.service == "cohere":
        # Call Cohere API
        return JSONResponse(content="OK")

host = os.getenv("HOST", "localhost")
port = os.getenv("PORT", 8000)


uvicorn.run(app, host=host, port=port)
