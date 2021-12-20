from sklearn.model_selection import train_test_split

from data_extractor import get_data
from embeddings_generator import Embedder
import create_model


def main() -> None:
    embedder = Embedder()

    df = get_data()
    X, y = df.drop("price", axis=1), df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

    embedder.create_embeddings(X,
                               X_train,
                               X_test,
                               y_train,
                               y_test)

    X = X.join(embedder.generate_features(X["brand"],
                                          X["series"])).drop(["brand", "series"], axis=1)
    # X_train = X_train.join(embedder.generate_features(X_train["brand"],
    #                                                   X_train["series"])).drop(["brand", "series"], axis=1)
    # X_test = X_test.join(embedder.generate_features(X_test["brand"],
    #                                                 X_test["series"])).drop(["brand", "series"], axis=1)

    create_model.fit_model(X, y)


if __name__ == "__main__":
    main()
