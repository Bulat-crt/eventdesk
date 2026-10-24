from sqlalchemy.orm import Session
from app.repositories.registration_repository import create_new_registration, get_event_by_id_for_update, get_registration_count_by_event, get_registrations_by_email
from app.repositories.event_repository import get_event_by_id
from app.exceptions import EventNotFoundError, EmailAlreadyRegisteredError, EventCapacityReachedError
from app.schemas import EventRegistrationStats

def register_attendee(
    session: Session,
    event_id: int,
    email: str,
    attendee_name: str
):
    try:
        event = get_event_by_id_for_update(session, event_id)

        if event is None:
            raise EventNotFoundError('Нет такого мероприятия')

        register = get_registrations_by_email(session, email, event_id)

        if register is not None:
            raise EmailAlreadyRegisteredError('Такой email уже зарегестрирован')

        count = get_registration_count_by_event(session, event_id)

        if count >= event.capacity:
            raise EventCapacityReachedError('Все места заняты')

        registration = create_new_registration(
            session=session, 
            attendee_name=attendee_name,
            attendee_email=email,
            event=event
        )

        session.commit()
        return registration
    except Exception:
        session.rollback()
        raise


def get_available_places(
    session: Session,
    event_id: int
) -> EventRegistrationStats:  
    event = get_event_by_id(session, event_id)
    if event is None:
        raise EventNotFoundError('Нет такого ивента')

    count = get_registration_count_by_event(session, event_id)

    available = event.capacity - count

    return EventRegistrationStats(
        event_id=event_id,
        registered_count=count,
        capacity=event.capacity,
        available_places=available
    )


