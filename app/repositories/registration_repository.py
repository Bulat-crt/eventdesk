from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import Registration, Event

def create_new_registration(
    session: Session,
    attendee_name: str,
    attendee_email: str,
    event: Event
) -> Registration:  
    registr = Registration(
        attendee_name=attendee_name,
        attendee_email=attendee_email,
        event_id=event.id
    )

    session.add(registr)

    session.flush()

    session.refresh(registr)

    return registr

def get_registration_by_id(
    session: Session,
    registr_id: int
) -> Registration | None:
    statement = select(Registration).where(Registration.id == registr_id)

    user = session.scalars(statement).first()

    return user


def get_registrations_by_event(
    session: Session,
    event: Event
) -> list[Registration]:
    statement = select(Registration).where(Registration.event_id == event.id)

    registrations = session.scalars(statement).all()

    return registrations


def get_registrations_by_email(
    session: Session,
    email: str,
    event_id: int
) -> Registration | None:
    statement = select(Registration).where(Registration.attendee_email == email, Registration.event_id == event_id)

    registrations = session.scalars(statement).first()

    return registrations


def get_event_by_id_for_update(
    session: Session,
    event_id: int
) -> Event | None:
    statement = select(Event).where(Event.id == event_id).with_for_update()

    event = session.scalars(statement).first()

    return event

def get_registration_count_by_event(
    session: Session,
    event_id: int
) -> int:
    statement = select(func.count(Registration.id)).where(Registration.event_id == event_id)

    count = session.scalar(statement)

    return count