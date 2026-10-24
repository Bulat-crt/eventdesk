from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Event(Base):
    __tablename__ = 'events'
    __table_args__ = (
        CheckConstraint(
            "capacity > 0",
            name="ck_events_capacity_positive"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    location: Mapped[str] = mapped_column(String(2048), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    registrations: Mapped[list['Registration']] = relationship(back_populates='event', cascade='all, delete-orphan')

class Registration(Base):
    __tablename__ = 'registrations'
    __table_args__ = (
    UniqueConstraint(
        "event_id",
        "attendee_email",
        name="uq_registration_event_email"
    ),
)

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    attendee_name: Mapped[str] = mapped_column(String(200), nullable=False)
    attendee_email: Mapped[str] = mapped_column(String(256), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    event: Mapped['Event'] = relationship(back_populates='registrations')