from typing import Optional
from typing import List
from fastapi import FastAPI, Body, status
from pydantic import BaseModel, Field
from enum import Enum

from fastapi.responses import JSONResponse, Response


from fastapi import FastAPI

app = FastAPI()

class DrawState(str, Enum):
    pending = "pending"
    onlive = "onlive"
    done = "done"

class Draw(BaseModel):
    id: int = Field(
        None, title="Unique identifier for a draw."
    )
    title: str = Field(
        None, title="Title for the event draw", max_length=100
    )
    dateat: str = Field(
        None, title="Date for the event draw", max_length=10
    )    
    status: DrawState = Field(
        None, title="State of the draw, could it be pending, onlive, or done."
    )    
    class Config:
        schema_extra = {
            "example": {
                "title": "Navidad 2020", 
                "dateat": "2020-12-17"
            }
        }


fake_draws_db = [
    {"id": 1, "title": "Navidad 2020", "dateat": "2020-12-17", "status":"pending"}, 
    {"id": 2, "title": "Aniversario 2021", "dateat": "2021-03-07", "status":"pending"}, 
    {"id": 3, "title": "Día del enzima", "dateat": "2021-05-10", "status":"pending"}
]

@app.get("/draws")
async def get_draws():
    return fake_draws_db

@app.post("/draws", status_code=201)
async def create_draw(draw: Draw):    
    draw.id = len(fake_draws_db) + 1
    draw.status = DrawState.pending
    fake_draws_db.append(draw)
    return draw

@app.put("/draws/{draw-id}")
async def update_draw(draw_id: int, draw: Draw):
    for index in range(len(fake_draws_db)):
        print(fake_draws_db[index])
        if fake_draws_db[index]['id'] == draw_id:
            fake_draws_db[index]['title'] = draw.title
            fake_draws_db[index]['dateat'] = draw.dateat
            return fake_draws_db[index]
    return JSONResponse(status_code=404, content=draw_id)

@app.get("/draws/{draw-id}", status_code=200)
async def get_draw(draw_id: int):
    for draw in fake_draws_db:
        if draw['id'] == draw_id:        
            return draw
    return JSONResponse(status_code=404, content=draw_id)

@app.delete("/draws/{draw-id}")
async def remove_draw(draw_id: int):
    for index in range(len(fake_draws_db)):
        if fake_draws_db[index]['id'] == draw_id:
            fake_draws_db.pop(index)
            break
    return Response(status_code=204)