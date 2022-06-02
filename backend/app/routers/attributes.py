from ..schemas import attribute as attribute_schemas
from ..schemas import user as user_schemas
from ..repositories import attributes as attributes_repository
from ..dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from ..auth.auth import get_current_active_user

router = APIRouter()


@router.get("/attributes/", response_model=list[attribute_schemas.Attribute])
def get_attributes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: user_schemas.User = Security(get_current_active_user, scopes=["attributes:read"])):
    attributes = attributes_repository.get_attributes(
        db, skip=skip, limit=limit)
    return attributes


@router.get("/attributes/{attribute_id}", response_model=attribute_schemas.Attribute)
def get_attribute_by_id(attribute_id: int, db: Session = Depends(get_db), user: user_schemas.User = Security(get_current_active_user, scopes=["attributes:read"])):
    db_attribute = attributes_repository.get_attribute_by_id(
        db, attribute_id=attribute_id)
    if db_attribute is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found")
    return db_attribute


@router.post("/attributes/", response_model=attribute_schemas.Attribute)
def create_attribute(attribute: attribute_schemas.AttributeCreate, db: Session = Depends(get_db), user: user_schemas.User = Security(get_current_active_user, scopes=["attributes:create"])):
    return attributes_repository.create_attribute(db=db, attribute=attribute)
