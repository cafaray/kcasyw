from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Draw(BaseModel):
    title: str = Field(
        None, title="Title for the event draw", max_length=100
    )
    dateat: str = Field(
        None, title="Date for the event draw", max_length=10
    )    

@app.post("/draws")
async def create_draw(draw: Draw):
    return draw

@app.put("/draws/{draw-id}")
async def update_draw(draw_id: int, draw: Draw):
    return {"draw-id": draw_id, **draw.dict() }