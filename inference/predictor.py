import os

import lightgbm
from pandas import DataFrame


class Predictor:
    def __init__(self, base_dir: str, filename: str) -> None:
        path = os.path.join(base_dir, filename)
        self.model = lightgbm.Booster(model_file=path)

    def predict(self, df: DataFrame) -> float:
        return self.model.predict(df)[0]
