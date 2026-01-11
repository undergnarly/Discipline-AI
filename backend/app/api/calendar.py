from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from .. import database, models, schemas
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/calendar", tags=["Calendar"])

# Здесь будет логика для CRUD операций с календарем.
# Пока это заглушки, чтобы создать "скелет" API.

@router.post("/events", response_model=schemas.CalendarEventInDB, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: schemas.CalendarEventCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # TODO: Реализовать создание события
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/events", response_model=List[schemas.CalendarEventInDB])
async def read_events(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    # TODO: Реализовать получение событий
    raise HTTPException(status_code=501, detail="Not implemented")

@router.put("/events/{event_id}", response_model=schemas.CalendarEventInDB)
async def update_event(
    event_id: uuid.UUID,
    event: schemas.CalendarEventUpdate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # TODO: Реализовать обновление события
    raise HTTPException(status_code=501, detail="Not implemented")

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: uuid.UUID,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # TODO: Реализовать удаление события
    raise HTTPException(status_code=501, detail="Not implemented") 