from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import EventCreate, EventResponse
from app.exceptions import EventNotFoundError
from app.database import get_db
from app.services.event_service import create_new_event, find_event, all_events, delete_current_event

router = APIRouter()

@router.post('/events', response_model=EventResponse, status_code=201)
def add_event(
    event: EventCreate,
    session: Session = Depends(get_db)
):
    return create_new_event(session, event)

@router.get('/events', response_model=list[EventResponse])
def get_all_events(session: Session = Depends(get_db)):
    return all_events(session)

@router.get('/events/{event_id}', response_model=EventResponse)
def get_event_by_event_id(
    event_id: int, 
    session: Session = Depends(get_db)
):
    try:
        event = find_event(session, event_id)
    except EventNotFoundError:
        raise HTTPException(
            status_code=404,
            detail='Нет такого ивента'
        )

    return event

@router.delete('/events/{event_id}', status_code=204)
def delete_event(
    event_id: int,
    session: Session = Depends(get_db)
):
    try:
        delete_current_event(session, event_id)
    except EventNotFoundError:
        raise HTTPException(
            status_code=404,
            detail='Нет такого ивента'
        )

    