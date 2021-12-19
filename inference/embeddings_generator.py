import pickle
import os

import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding
from tensorflow.keras.callbacks import EarlyStopping

from utils import rm_spaces


class Embedder:
    """"""

    def __init__(self) -> None:
        self.brand_dim: int
        self.series_dim: int
        self.embedding_layer_brand: tf.keras.layers.Layer
        self.embedding_layer_series: tf.keras.layers.Layer
        self.num_series: int
        self.num_brand: int
        self.series_tokenizer: Tokenizer
        self.brand_tokenizer: Tokenizer
        self.feature_generator_brand: tf.keras.Model
        self.feature_generator_series: tf.keras.Model

        self.output_path = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def _make_brand_tokenizer(self, series: pd.Series) -> None:
        """Takes in a pandas Series object and creates and stores a tokenizer"""
        tokenizer = Tokenizer(oov_token="<OOV>")
        tokenizer.fit_on_texts(series.apply(lambda x: rm_spaces(x)))
        self.num_brand = len(tokenizer.word_index)
        self.brand_tokenizer = tokenizer
        with open(os.path.join(self.output_path, 'tokenizer_brand.pkl'), 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def set_brand_tokenizer(self, tokenizer: Tokenizer) -> None:
        """Takes in a serialized tokenizer object,
        for when we don't want to re-create the tokenizer"""
        self.brand_tokenizer = tokenizer

    def get_brand_tokens(self, series: pd.Series) -> tf.Tensor:
        if self.brand_tokenizer is None:
            self._make_brand_tokenizer(series)
        tokens = self.brand_tokenizer.texts_to_sequences(series.apply(lambda x: rm_spaces(x)))
        return tf.squeeze(tf.constant(tokens))

    def _make_series_tokenizer(self, series: pd.Series) -> None:
        """Takes in a pandas Series object and creates and stores a tokenizer"""
        tokenizer = Tokenizer(oov_token="<OOV>")
        tokenizer.fit_on_texts(series.apply(lambda x: rm_spaces(x)))
        self.num_series = len(tokenizer.word_index)
        self.series_tokenizer = tokenizer
        with open(os.path.join(self.output_path, 'tokenizer_series.pkl'), 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def set_series_tokenizer(self, tokenizer: Tokenizer) -> None:
        """Takes in a serialized tokenizer object,
        for when we don't want to re-create the tokenizer"""
        self.series_tokenizer = tokenizer

    def get_series_tokens(self, series: pd.Series) -> tf.Tensor:
        if self.series_tokenizer is None:
            self._make_series_tokenizer(series)
        tokens = self.series_tokenizer.texts_to_sequences(series.apply(lambda x: rm_spaces(x)))
        return tf.squeeze(tf.constant(tokens))

    def _create_model(self, brand_dim: int = 5, series_dim: int = 15) -> tf.keras.Model:
        self.brand_dim = brand_dim
        self.series_dim = series_dim

        input_brand = tf.keras.layers.Input(shape=(1,))
        input_series = tf.keras.layers.Input(shape=(1,))
        embedding_brand = Embedding(input_dim=self.num_brand + 1,
                                    output_dim=brand_dim,
                                    name='embedding_brand')(input_brand)
        embedding_series = Embedding(input_dim=self.num_series + 1,
                                     output_dim=series_dim,
                                     name='embedding_series')(input_series)
        concat = tf.keras.layers.Concatenate()([embedding_brand, embedding_series])
        output = tf.keras.layers.Dense(1)(concat)
        model = tf.keras.Model(inputs=[input_brand, input_series],
                               outputs=output)
        model.compile(loss='mean_squared_error',
                      optimizer=tf.keras.optimizers.Adam(lr=3e-4),
                      metrics=[tf.keras.metrics.RootMeanSquaredError()])

        return model

    def create_embeddings(self,
                          brand_train_tokens: tf.Tensor,
                          brand_test_tokens: tf.Tensor,
                          series_train_tokens: tf.Tensor,
                          series_test_tokens: tf.Tensor,
                          y_train: pd.Series,
                          y_test: pd.Series
                          ) -> None:
        early_stopping = EarlyStopping(patience=30, restore_best_weights=True)
        model = self._create_model()
        model.fit((brand_train_tokens, series_train_tokens),
                  y_train.to_numpy(),
                  validation_data=((brand_test_tokens, series_test_tokens),
                                   y_test.to_numpy()),
                  epochs=3000,
                  callbacks=[early_stopping],
                  verbose=2)

        embedding_layer_brand = model.get_layer('embedding_brand')
        embedding_layer_brand.trainable = False
        self.embedding_layer_brand = embedding_layer_brand

        embedding_layer_series = model.get_layer('embedding_series')
        embedding_layer_series.trainable = False
        self.embedding_layer_series = embedding_layer_series

    def create_feature_generators(self):
        self.feature_generator_brand = tf.keras.models.Sequential([
            tf.keras.layers.InputLayer(input_shape=[1, ]),
            self.embedding_layer_brand
        ])
        self.feature_generator_series = tf.keras.models.Sequential([
            tf.keras.layers.InputLayer(input_shape=[1, ]),
            self.embedding_layer_series
        ])

    def set_feature_generators(self, feature_generator_brand: tf.keras.Model,
                               feature_generator_series: tf.keras.Model) -> None:
        self.feature_generator_brand = feature_generator_brand
        self.feature_generator_series = feature_generator_series
        self.brand_dim = feature_generator_brand.get_layer('embedding_brand').output_shape[2]
        self.series_dim = feature_generator_brand.get_layer('embedding_series').output_shape[2]

    def generate_features(self, brand: pd.Series, series: pd.Series) -> pd.DataFrame:
        if self.feature_generator_brand is None or self.feature_generator_series is None:
            raise Exception("""No feature generators. Either set a pair of generators 
                            with set_feature_generators(), or create them with 
                            create_embeddings() and create_feature_generators()""")

        brand_tokens = self.get_brand_tokens(brand)
        brand_array = np.squeeze(brand_tokens, axis=1)
        series_tokens = self.get_series_tokens(series)
        series_array = np.squeeze(series_tokens, axis=1)
        features_array = np.concatenate((brand_array, series_array), axis=1)

        embedding_cols = ["brand_embedding_" + str(i + 1) for i in range(self.brand_dim)] + \
                         ["series_embedding_" + str(i + 1) for i in range(self.series_dim)]

        return pd.DataFrame(features_array, columns=embedding_cols)

def api(self):
    # create tokenizers with full x
    # get tokens for each brand, label, train, test
    pass

