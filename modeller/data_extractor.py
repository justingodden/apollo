import pandas as pd


def get_data() -> pd.DataFrame:
    sqlite_file_name = "../scraper/database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    df = pd.read_sql_table('watch', sqlite_url)
    df.drop(['id', 'model_num', 'model_id', 'product_url', 'image_url', 'image_filename'], axis=1, inplace=True)
    df = df.astype({
        'brand': 'category',
        'series': 'category',
    })
    df["box"] = df["box"].map({True: 1, False: 0})
    df["papers"] = df["papers"].map({True: 1, False: 0})
    return df
