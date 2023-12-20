from tools import db_tools, db
from pylon.core.tools import log

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(db_tools.AbstractBaseMixin, db.Base):
    __tablename__ = 'social_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

