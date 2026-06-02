from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

import pandas as pd
import joblib

app = FastAPI()
model = joblib.load("house_price_pipeline.pkl")
df = pd.read_csv("Housing.csv")

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
def home():
    with open("templates/index.html","r",encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

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
    percentile = ((df["price"] < prediction).sum()/len(df)) * 100
    return {"price": float(prediction),"percentile": float(percentile)}