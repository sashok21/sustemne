from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer

int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

class BaseModel(DeclarativeBase):

    pass

