from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.infrastructure.db.database import generate_snowflake_id


class BaseMixin:
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
        onupdate=func.now(), nullable=True
    )

class Base(DeclarativeBase):
    ...

class BoardEntity(BaseMixin, Base):
    __tablename__ = "boards"

    name: Mapped[str] = mapped_column(index=True)
    position: Mapped[int] = mapped_column(nullable=False, default=0)

    tasks: Mapped[List["TaskEntity"]] = relationship(
        back_populates="board", lazy="subquery",
        order_by="TaskEntity.position")


class TaskEntity(BaseMixin, Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(nullable=False, default=0)

    board_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("boards.id"), index=True, nullable=False)

    board: Mapped["BoardEntity"] = relationship(
        back_populates="tasks", lazy="joined")
