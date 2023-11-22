import chatgpt_adapter
import pandas as pd
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/hello")
def hello():
    return {"Kakaomobility Hackerton 2023": "공통통"}


@app.get("/api/parking-lot/area")
def get_parking_summary():
    with open("data/parking_review_summary.json", 'r', encoding='utf-8') as file:
        summary = json.load(file)
        suggest = chatgpt_adapter.get_parking_suggest("아반떼")
        # 좌표, 이미지 URL
        return {"summary": summary, "suggest": json.loads(suggest)}


@app.post("/api/parking/summary")
def get_parking_summary():
    # TODO: 기능 개선
    # 1. raw_data 디렉토리에서 파일을 찾는다.
    # 2. 이미 json 파일이 만들어졌으면 스킵한다. 없으면 chatgpt에 요청해서 요약정보를 저장한다.
    # 3. rate limit를 회피하기 위해 1회 요청 이후 약 30초 정도 쉬었다가 이어서 시도한다.
    # 4. 디렉토리에서 json 파일을 모두 찾아서 합친다.
    filename = "data/주차평가5점주관식-하이파킹 판교알파돔타워"
    data = pd.read_csv(filename + ".csv")

    summary = chatgpt_adapter.get_parking_summary(data)
    summary_json = json.loads(summary)
    with open(filename + ".json", "w") as file:
        json.dump(summary_json, file, ensure_ascii=False)
