from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4


app = FastAPI()

class Bot(BaseModel):
    id: Optional[UUID] = None
    question: str
    answer: str


responses = []


@app.post("/ask-question/", response_model = Bot)
def create_bot(bot: Bot):
    bot.id = uuid4()
    responses.append(bot)
    return bot

@app.get("/get-responses/", response_model = List[Bot])
def read_bot():
    return responses


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)