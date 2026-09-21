from sqlalchemy.orm import Session

from app.repositories.admin_repository import (
    get_all_users,
    get_all_documents,
    get_system_logs_summary,
)


def list_all_users_service(db: Session):
    return get_all_users(db)


def list_all_documents_service(db: Session):
    return get_all_documents(db)


def get_admin_logs_service(db: Session):
    summary = get_system_logs_summary(db)

    return {
        "message": "System logs summary fetched successfully",
        "data": summary
    }