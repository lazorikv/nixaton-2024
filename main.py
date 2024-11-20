from fastapi import FastAPI
from fastapi.params import Body

from models import Input, Output
from parser import parse_data

app = FastAPI()


@app.get("/healthz")
async def root():
    return {"status": "OK"}


@app.post("/move")
async def move(input: Input) -> Output:
    parsed_data = parse_data(input)
    return Output("M")
