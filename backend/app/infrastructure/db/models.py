from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.database import generate_snowflake_id


class BaseMixin(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=generate_snowflake_id,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), nullable=False
    )


class BoardEntity(BaseMixin):
    __tablename__ = "boards"

    name: Mapped[str] = mapped_column(index=True)
    position: Mapped[int] = mapped_column(nullable=False, default=0)


class TaskEntity(BaseMixin):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(nullable=False, default=0)

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"), index=True, nullable=False)
