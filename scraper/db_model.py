from typing import Optional

from sqlmodel import Field, SQLModel


class Watch(SQLModel, table=True):
    __tablename__ = "watches"

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
