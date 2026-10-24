from app.schemas import RegistrationCreate, RegistrationResponse, EventRegistrationStats
from app.services.registration_service import register_attendee, get_available_places
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.exceptions import EventCapacityReachedError, EmailAlreadyRegisteredError, EventNotFoundError

router = APIRouter()

@router.post('/events/{event_id}/registrations', response_model=RegistrationResponse, status_code=201)
def create_registr(
    data_reg: RegistrationCreate,
    event_id: int,
    session: Session = Depends(get_db)
):
    try:
        succes = register_attendee(
            session=session,
            event_id=event_id,
            email=data_reg.attendee_email,
            attendee_name=data_reg.attendee_name
        )
    except EventNotFoundError:
        raise HTTPException(
            status_code=404,
            detail='Нет такого ивента'
        )
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=409,
            detail='Email уже зарегестрирован на данное мероприятие'
        )
    except EventCapacityReachedError:
        raise HTTPException(
            status_code=409,
            detail='Все места уже заняты'
        )

    return succes

@router.get('/events/{event_id}/registrations/stats', response_model=EventRegistrationStats)
def get_stats_of_event(
    event_id: int,
    session: Session = Depends(get_db)
):  
    try:
        answer = get_available_places(session, event_id)
    except EventNotFoundError:
        raise HTTPException(
            status_code=404,
            detail='Нет такого ивента'
        )

    return answer