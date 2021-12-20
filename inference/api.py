import datetime
import os

import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn


from feature_engineering import FeatureEngineering
from predictor import Predictor


BASE_DIR = os.path.join(os.path.dirname(os.getcwd()), "modeller", "output")


class Watch(BaseModel):
    brand: str
    series: str
    year: int
    box: bool
    papers: bool


app = FastAPI()

feature_engineering = FeatureEngineering(base_dir=BASE_DIR,
                                         brand_tokenizer_filename="tokenizer_brand.pkl",
                                         series_tokenizer_filename="tokenizer_series.pkl",
                                         brand_embedding_model_name="feature_generator_brand",
                                         series_embedding_model_name="feature_generator_series"
                                         )
predictor = Predictor(base_dir=BASE_DIR,
                      filename="lgb_model.txt")


@app.get("/")
def root():
    return f"""
    <html>
        <head>
            <title>Apollo - The Watch Pricing Specialist</title>
        </head>
        <body>
            <p>&copy; Apollo {datetime.datetime.utcnow().year} v.3000.04</p>
        </body>
    </html>
    """.replace("\n", "")


@app.get("/predict")
def predict(watch: Watch) -> float:
    watch_df = pd.DataFrame(watch.dict(), index=[0])
    watch_df = watch_df.join(feature_engineering.generate_features(watch_df["brand"],
                                                                   watch_df["series"])).drop(["brand", "series"],
                                                                                             axis=1)
    watch_df["box"] = watch_df["box"].map({True: 1, False: 0})
    watch_df["papers"] = watch_df["papers"].map({True: 1, False: 0})
    return predictor.predict(watch_df)


def main():
    uvicorn.run("api:app")


if __name__ == "__main__":
    main()
