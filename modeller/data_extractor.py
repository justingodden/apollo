import pandas as pd
from sqlalchemy import create_engine

from secret import get_secret


def get_data() -> pd.DataFrame:
    mysql_url = get_secret()
    engine = create_engine(mysql_url)
    df = pd.read_sql_table('watch', con=engine)
    df.drop(['id', 'model_num', 'model_id', 'product_url', 'image_url', 'image_filename'], axis=1, inplace=True)
    df = df.astype({
        'brand': 'category',
        'series': 'category',
    })
    df["box"] = df["box"].map({True: 1, False: 0})
    df["papers"] = df["papers"].map({True: 1, False: 0})
    return df
