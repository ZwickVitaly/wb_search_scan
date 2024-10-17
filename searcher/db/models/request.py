from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from ..base import Base


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    query: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)

