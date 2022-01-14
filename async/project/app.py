from fastapi import FastAPI, Query
from project.monitoring import instrumentator
from project.sentiment.model import SentimentBertModel
from starlette.responses import JSONResponse

app = FastAPI()
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


@app.post("/")
async def predict_sentiment(input_text: str = Query(..., min_length=2)):
    classifier = SentimentBertModel("distilbert-base-uncased-finetuned-sst-2-english")
    out_dict = classifier.predict(input_text)
    return JSONResponse(out_dict)


@app.get("/healthcheck", status_code=200)
async def healthcheck():
    return "dummy check! Classifier is all ready to go!"
