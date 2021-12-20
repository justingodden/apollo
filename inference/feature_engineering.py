import pickle
import os
import re

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model


class FeatureEngineering:
    """"""
    def __init__(self,
                 base_dir: str,
                 brand_tokenizer_filename: str,
                 series_tokenizer_filename: str,
                 brand_embedding_model_name: str,
                 series_embedding_model_name: str
                 ) -> None:
        self.brand_tokenizer: Tokenizer = self.load_tokenizer(base_dir=base_dir,
                                                              filename=brand_tokenizer_filename)
        self.series_tokenizer: Tokenizer = self.load_tokenizer(base_dir=base_dir,
                                                               filename=series_tokenizer_filename)
        self.feature_generator_brand: Model = self.load_embedding_model(base_dir=base_dir,
                                                                        filename=brand_embedding_model_name)
        self.feature_generator_series: Model = self.load_embedding_model(base_dir=base_dir,
                                                                         filename=series_embedding_model_name)
        self.brand_dim: int = self.feature_generator_brand.get_layer("embedding_brand").output_shape[2]
        self.series_dim: int = self.feature_generator_series.get_layer("embedding_series").output_shape[2]

    @staticmethod
    def load_tokenizer(base_dir: str, filename: str) -> Tokenizer:
        path = os.path.join(base_dir, filename)
        with open(path, "rb") as handle:
            tokenizer = pickle.load(handle)
        return tokenizer

    @staticmethod
    def load_embedding_model(base_dir: str, filename: str) -> Model:
        path = os.path.join(base_dir, filename)
        return load_model(path, compile=False)

    def get_brand_tokens(self, series: pd.Series) -> tf.Tensor:
        tokens = self.brand_tokenizer.texts_to_sequences(series.apply(lambda x: rm_spaces(x)))
        return tf.squeeze(tf.constant(tokens))

    def get_series_tokens(self, series: pd.Series) -> tf.Tensor:
        tokens = self.series_tokenizer.texts_to_sequences(series.apply(lambda x: rm_spaces(x)))
        return tf.squeeze(tf.constant(tokens))

    def generate_features(self, brand: pd.Series, series: pd.Series) -> pd.DataFrame:
        brand_tokens = self.get_brand_tokens(brand)
        brand_tokens = tf.expand_dims(brand_tokens, axis=0)
        brand_array = self.feature_generator_brand.predict(brand_tokens)
        brand_array = np.squeeze(brand_array, axis=1)

        series_tokens = self.get_series_tokens(series)
        series_tokens = tf.expand_dims(series_tokens, axis=0)
        series_array = self.feature_generator_series.predict(series_tokens)
        series_array = np.squeeze(series_array, axis=1)

        features_array = np.concatenate((brand_array, series_array), axis=1)

        embedding_cols = ["brand_embedding_" + str(i + 1) for i in range(self.brand_dim)] + \
                         ["series_embedding_" + str(i + 1) for i in range(self.series_dim)]

        return pd.DataFrame(features_array, columns=embedding_cols, index=brand.index)


def rm_spaces(feature: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]", "", feature)
