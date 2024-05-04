import uuid
import datetime

from sqlalchemy import Uuid, String, Numeric, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db import Base


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    salary: Mapped[float] = mapped_column(
        Numeric,
        nullable=False
    )
    days_to_promotion: Mapped[datetime.timedelta] = mapped_column(
        Interval,
        nullable=False
    )

    user = relationship('UserJob', cascade='all, delete')


class UserJob(Base):
    __tablename__ = 'user_job'

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        index=True,
        nullable=False
    )
    job_id: Mapped[Uuid] = mapped_column(
        ForeignKey('jobs.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )

