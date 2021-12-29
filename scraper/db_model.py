from typing import Optional

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


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def add_to_db(watch: Watch) -> None:
    with Session(engine) as session:
        session.add(watch)
        session.commit()


def url_exists_in_db(url: str) -> bool:
    with Session(engine) as session:
        watch = session.exec(select(Watch).where(
            Watch.product_url == url)).first()
        return True if watch else False
