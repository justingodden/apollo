import os

import pandas as pd
from sklearn.model_selection import KFold
from lightgbm import early_stopping
from lightgbm import log_evaluation
import optuna.integration.lightgbm as lgb_tuner

import s3


def fit_model(X: pd.DataFrame, y: pd.Series) -> None:
    dtrain = lgb_tuner.Dataset(X, label=y)

    params = {
        "objective": "regression",
        "metric": "mean_squared_error",
        "boosting_type": "gbdt",
    }

    tuner = lgb_tuner.LightGBMTunerCV(params,
                                      dtrain,
                                      num_boost_round=3000,
                                      folds=KFold(n_splits=5),
                                      callbacks=[early_stopping(100),
                                                 log_evaluation(100)],
                                      return_cvbooster=True
                                      )

    tuner.run()

    model = tuner.get_best_booster()

    output_path = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    file_name = "lgb_model.txt"
    file_path = os.path.join(output_path, file_name)
    model.save_model(file_path)
    s3.upload_file(file_path=file_path, key_name=file_name)
