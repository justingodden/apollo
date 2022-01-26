from typing import Optional, List
from collections import defaultdict

from sqlmodel import Field, Session, SQLModel, create_engine, select

from secret import get_secret


class Watch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_url: str
    brand: str
    series: str
    model_num: str
    model_id: str
    price: int
    year: int
    box: bool
    papers: bool
    image_url: str
    image_filename: str


sql_uri = get_secret()

engine = create_engine(sql_uri, echo=False)


def _query_db() -> List[tuple]:
    with Session(engine) as session:
        statement = select(Watch.brand, Watch.series)
        return session.exec(statement).all()


def _group_by(data: List[tuple]) -> defaultdict:
    data = list(set([tup for tup in data]))  # dedupe
    data = sorted(data)
    d = defaultdict(list)
    for k, v in data:
        d[k].append(v)
    return d


def get_brand_and_series() -> defaultdict:
    return _group_by(_query_db())
