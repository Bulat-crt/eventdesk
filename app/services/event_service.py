from app.repositories.event_repository import create_event, get_all_events, get_event_by_id, delete_event
from sqlalchemy.orm import Session
from app.schemas import EventCreate
from app.exceptions import EventNotFoundError
from app.models import Event

def create_new_event(
    session: Session,
    event: EventCreate
) -> Event:
    return create_event(
        session=session,
        title=event.title,
        location=event.location,
        starts_at=event.starts_at,
        capacity=event.capacity,
        description=event.description
    )

def find_event(
    session: Session,
    event_id: int
) -> Event:
    event = get_event_by_id(session, event_id)

    if event is None:
        raise EventNotFoundError('Нет такого ивента')

    return event

def all_events(session: Session) -> list[Event]:
    return get_all_events(session)

def delete_current_event(
    session: Session, 
    event_id: int
):
    event = get_event_by_id(session, event_id)

    if event is None:
        raise EventNotFoundError('Нет такого ивента')

    delete_event(session, event)
