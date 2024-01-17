from datetime import datetime
from tools import db_tools, db
from sqlalchemy import Integer, String, DateTime, func, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column


class Feedback(db_tools.AbstractBaseMixin, db.Base):
    __tablename__ = 'social_feedbacks'
    __table_args__ = (
        UniqueConstraint('page', 'user_id', 'project_id',
                         name='_feedback_page_uc'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    page: Mapped[int] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
