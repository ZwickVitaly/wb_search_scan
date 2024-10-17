from datetime import date

from sqlalchemy import Integer, ForeignKey, Date, func, String, ARRAY
from sqlalchemy.orm import mapped_column, Mapped

from ..base import Base


class RequestProduct(Base):
    __tablename__ = "request_product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete="CASCADE"))
    query: Mapped[str] = mapped_column(String)
    products: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    positions: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    natural_positions: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    date: Mapped[date] = mapped_column(Date, server_default=func.now())