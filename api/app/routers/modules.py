from typing import Optional

from app.auth.security import get_current_active_user
from app.db.session import get_db
from app.repositories import modules as modules_repository
from app.schemas import module as module_schemas
from app.schemas import user as user_schemas
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

router = APIRouter()


async def get_modules_parameters(
    enabled: Optional[bool] = None,
):
    return {"enabled": enabled}


@router.get("/modules/", response_model=list[module_schemas.Module])
async def get_modules(
    params: dict = Depends(get_modules_parameters),
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["modules:read"]
    ),
) -> list[module_schemas.Module]:

    return modules_repository.get_modules(db, params["enabled"])


@router.patch("/modules/{module_name}")
async def update_module(
    module_name: str,
    module: module_schemas.ModuleSettingsUpdate,
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["modules:update"]
    ),
):
    return modules_repository.update_module(
        db=db, module_name=module_name, module=module
    )


@router.post("/modules/query")
async def query_module(
    query: module_schemas.ModuleQuery,
    db: Session = Depends(get_db),
    user: user_schemas.User = Security(
        get_current_active_user, scopes=["modules:query"]
    ),
):
    return modules_repository.query_module(db, query=query)
