from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()


responses = []

class Bot(BaseModel):
    question: str
    answer: str

@app.post("/ask-question/{question}", response_model=Bot)
def ask_bot(question: str) -> Bot:
    model = OllamaLLM(model="llama3")
    context = ""
    
    template = """
        You are a AI bot which will help user to plan their diet and workout.
            Here is the conversation history: {context}

            Question: {question}

            Answer: 
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = prompt | model
    answer = chain.invoke({"context": context, "question": question})
    responses.append(answer)
    return Bot(question=question, answer=answer)
    
    
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)