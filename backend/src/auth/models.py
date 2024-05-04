import uuid
import datetime

from sqlalchemy import func
from sqlalchemy import Uuid, String, Boolean, Date, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    date_of_employment: Mapped[datetime.date] = mapped_column(
        Date,
        server_default=func.now(),
        nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        index=True,
        default=False,
        nullable=False
    )
    is_staff: Mapped[bool] = mapped_column(
        Boolean,
        index=True,
        default=True,
        nullable=False
    )

    token = relationship('Token', cascade='all, delete')
    job = relationship('UserJob', cascade='all, delete')


class Token(Base):
    __tablename__ = 'access_tokens'

    key: Mapped[str] = mapped_column(
        String(128),
        primary_key=True
    )
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        index=True,
        nullable=False
    )

