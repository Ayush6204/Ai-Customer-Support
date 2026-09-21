from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import require_role
from app.schemas.admin_schema import (
    AdminUserResponse,
    AdminDocumentResponse,
    AdminLogResponse,
)
from app.services.admin_service import (
    list_all_users_service,
    list_all_documents_service,
    get_admin_logs_service,
)


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/users",
    response_model=list[AdminUserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"])),
):
    return list_all_users_service(db)


@router.get(
    "/documents",
    response_model=list[AdminDocumentResponse]
)
def get_all_documents(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"])),
):
    return list_all_documents_service(db)


@router.get(
    "/logs",
    response_model=AdminLogResponse
)
def get_logs(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"])),
):
    return get_admin_logs_service(db)