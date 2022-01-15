from fastapi import FastAPI
from project.monitoring import instrumentator
from project.sentiment.model import SentimentBertModel
from pydantic import BaseModel, constr
from starlette.responses import JSONResponse

app = FastAPI()
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


class Input(BaseModel):
    input_text: constr(min_length=2)


@app.post("/")
async def predict_sentiment(data: Input):
    classifier = SentimentBertModel("distilbert-base-uncased-finetuned-sst-2-english")
    out_dict = classifier.predict(data.input_text)
    return JSONResponse(out_dict)


@app.get("/healthcheck", status_code=200)
async def healthcheck():
    return "dummy check! Classifier is all ready to go!"
