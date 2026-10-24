from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from app.models import Event


def create_event(
    session: Session,
    title: str,
    location: str,
    starts_at: datetime,
    capacity: int,
    description: str | None
):
    event = Event(
        title=title,
        location=location,
        starts_at=starts_at,
        capacity=capacity,
        description=description
    )

    session.add(event)

    session.commit()

    session.refresh(event)

    return event



def get_event_by_id(
    session: Session,
    event_id: int
) -> Event | None:
    statement = select(Event).where(Event.id == event_id)

    event = session.scalars(statement).first()

    return event


def get_all_events(session: Session) -> list[Event]:
    statement = select(Event)

    all_events = session.scalars(statement).all()

    return all_events

def delete_event(
    session: Session,
    event: Event
):

    session.delete(event)

    session.commit()