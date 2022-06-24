from app.auth.auth import get_current_active_user
from app.dependencies import get_db
from app.repositories import attributes as attributes_repository
from app.repositories import events as events_repository
from app.schemas import attribute as attribute_schemas
from app.schemas import user as user_schemas
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/attributes/", response_model=list[attribute_schemas.Attribute])
def get_attributes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["attributes:read"]
    ),
):
    return attributes_repository.get_attributes(db, skip=skip, limit=limit)


@router.get("/attributes/{attribute_id}", response_model=attribute_schemas.Attribute)
def get_attribute_by_id(
    attribute_id: int,
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["attributes:read"]
    ),
):
    db_attribute = attributes_repository.get_attribute_by_id(
        db, attribute_id=attribute_id
    )
    if db_attribute is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found"
        )
    return db_attribute


@router.post(
    "/attributes/", response_model=attribute_schemas.Attribute, status_code=201
)
def create_attribute(
    attribute: attribute_schemas.AttributeCreate,
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["attributes:create"]
    ),
):
    event = events_repository.get_event_by_id(db, event_id=attribute.event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    return attributes_repository.create_attribute(db=db, attribute=attribute)


@router.patch("/attributes/{attribute_id}", response_model=attribute_schemas.Attribute)
def update_attribute(
    attribute_id: int,
    attribute: attribute_schemas.AttributeUpdate,
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["attributes:update"]
    ),
):
    return attributes_repository.update_attribute(
        db=db, attribute_id=attribute_id, attribute=attribute
    )
