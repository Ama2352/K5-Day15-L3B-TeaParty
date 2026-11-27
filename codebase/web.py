from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, StringConstraints

from agent import answer


app = FastAPI(title="TeaParty Demo")


class DemoRequest(BaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4000)]


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: DemoRequest):
    return {"output": answer(request.text)["output"]}
