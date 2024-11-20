from fastapi import FastAPI

app = FastAPI()


@app.get("/healthz")
async def root():
    return {"status": "OK"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
