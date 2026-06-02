from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from pydantic import BaseModel

import pandas as pd
import joblib

app = FastAPI()
templates = Jinja2Templates(directory="templates")
model = joblib.load("house_price_pipeline.pkl")

class House(BaseModel):
    area:int
    bedrooms:int
    bathrooms:int
    stories:int
    mainroad:int
    guestroom:int
    basement:int
    hotwaterheating:int
    airconditioning:int
    parking:int
    prefarea:int
    furnishingstatus:int


@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/predict")
def predict(house:House):
    data = pd.DataFrame(
        [[
            house.area,
            house.bedrooms,
            house.bathrooms,
            house.stories,
            house.mainroad,
            house.guestroom,
            house.basement,
            house.hotwaterheating,
            house.airconditioning,
            house.parking,
            house.prefarea,
            house.furnishingstatus
        ]],
        columns=[
            "area",
            "bedrooms",
            "bathrooms",
            "stories",
            "mainroad",
            "guestroom",
            "basement",
            "hotwaterheating",
            "airconditioning",
            "parking",
            "prefarea",
            "furnishingstatus"
        ]
    )

    prediction = model.predict(data)[0]
    return {"price":float(prediction)}