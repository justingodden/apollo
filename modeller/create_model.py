import os

import pandas as pd
from sklearn.model_selection import KFold
from lightgbm import early_stopping
from lightgbm import log_evaluation
import optuna.integration.lightgbm as lgb_tuner


def fit_model(X: pd.DataFrame, y: pd.Series):
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
                                                 log_evaluation(100)
                                                 ],
                                      return_cvbooster=True
                                      )

    tuner.run()

    model = tuner.get_best_booster()

    output_path = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    model.save_model(os.path.join(output_path, "lgb_model.txt"))
    # best_score_rmse = tuner.best_score**0.5
    # best_params = tuner.best_params
    # print(best_score_rmse)
