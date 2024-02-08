import uuid
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database.models.models import User
from app.dtos.UserDTO import UserCreationRequest, UserResponse
from app.repository.user_repository import UserRepository


def create_base_user(user_request: UserCreationRequest) -> User:
    return User(
        name=user_request.name,
        email=user_request.email,
        mobile=user_request.mobile
    )


async def create_user(user_request: UserCreationRequest, db: Session):
    user_repo = UserRepository(db)
    user: User = create_base_user(user_request)
    user.id = uuid.uuid4()
    try:
        created_user: Optional[User] = await run_in_threadpool(user_repo.create_user, user)
        if not created_user:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="User not created")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return UserResponse(
        id=created_user.id,
        name=created_user.name,
        email=created_user.email,
        mobile=created_user.mobile,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at,
    )


async def get_user_by_id(user_id: UUID, db: Session):
    user_repo = UserRepository(db)
    user: Optional[User] = await run_in_threadpool(user_repo.get_user_by_id, str(user_id))
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
