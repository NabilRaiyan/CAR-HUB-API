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

class Add(BaseModel):
    number: int
    answer: int
    
@app.post("/get/{number}")
def add(number: int)-> Add:
    result = number * number
    return Add(number=number, answer=result)

@app.post("/ask-question/{question}", response_model=Bot)
def ask_bot(question: str) -> Bot:
    try:
        template = """
        You are a AI bot which will help user to plan their diet and workout.
            Here is the conversation history: {context}

            Question: {question}

            Answer: 
        """
        model = OllamaLLM(model="llama3")
        context = ""
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        answer = chain.invoke({"context": context, "question": question})
        return Bot(question=question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

