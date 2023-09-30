from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class DDB(Base):
    __tablename__ = "DDB_List"
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(100))
    host: Mapped[str] = mapped_column(String(35))
    category: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return (f"Link: {repr(self.link)}, Host: {repr(self.host)}, Category: {repr(self.category)}")
