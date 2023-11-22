from fastapi import FastAPI
import chatgpt_adapter

import json

app = FastAPI()


@app.get("/")
def hello():
    return {"Kakaomobility Hackerton 2023": "공통통"}


@app.get("/parking/summary")
def get_parking_summary():
    with open("summary.json", 'r', encoding='utf-8') as file:
        summary = json.load(file)
        return {"summary": summary}


@app.get("/openai/talk")
def get_parking_summary():
    text_prompt = "Should oxford commas always be used?"
    return chatgpt_adapter.request(text_prompt)
