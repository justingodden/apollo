import datetime
import os

import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mangum import Mangum

from feature_engineering import FeatureEngineering
from predictor import Predictor
import s3
import database

output_path = os.path.join(os.getcwd(), "output")
brand_tokenizer_filename = "tokenizer_brand.pkl"
series_tokenizer_filename = "tokenizer_series.pkl"
brand_embedding_model_name = "feature_generator_brand.h5"
series_embedding_model_name = "feature_generator_series.h5"
lgb_model_filename = "lgb_model.txt"


class Watch(BaseModel):
    brand: str
    series: str
    year: int
    box: bool
    papers: bool


app = FastAPI()


def download_all() -> None:
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    s3.download_file(file_path=os.path.join(output_path, brand_tokenizer_filename),
                     key_name=brand_tokenizer_filename)
    s3.download_file(file_path=os.path.join(output_path, series_tokenizer_filename),
                     key_name=series_tokenizer_filename)
    s3.download_file(file_path=os.path.join(output_path, brand_embedding_model_name),
                     key_name=brand_embedding_model_name)
    s3.download_file(file_path=os.path.join(output_path, series_embedding_model_name),
                     key_name=series_embedding_model_name)
    s3.download_file(file_path=os.path.join(output_path, lgb_model_filename),
                     key_name=lgb_model_filename)


download_all()

feature_engineering = FeatureEngineering(base_dir=output_path,
                                         brand_tokenizer_filename=brand_tokenizer_filename,
                                         series_tokenizer_filename=series_tokenizer_filename,
                                         brand_embedding_model_name=brand_embedding_model_name,
                                         series_embedding_model_name=series_embedding_model_name
                                         )
predictor = Predictor(base_dir=output_path,
                      filename=lgb_model_filename)


@app.get("/brand-and-series.json")
def brand_and_series() -> dict:
    return database.get_brand_and_series()


@app.get("/")
def root() -> HTMLResponse:
    html_content = f"""
    <html>
        <head>
            <title>Apollo - The Watch Pricing Specialist</title>
        </head>
        <body>
            <p>&copy; Apollo {datetime.datetime.utcnow().year} v.0.0.1</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/predict")
def predict(watch: Watch) -> float:
    watch_df = pd.DataFrame(watch.dict(), index=[0])
    watch_df = watch_df.join(feature_engineering.generate_features(watch_df["brand"],
                                                                   watch_df["series"])).drop(["brand", "series"],
                                                                                             axis=1)
    watch_df["box"] = watch_df["box"].map({True: 1, False: 0})
    watch_df["papers"] = watch_df["papers"].map({True: 1, False: 0})
    pred = predictor.predict(watch_df)
    return round(pred)


handler = Mangum(app)
