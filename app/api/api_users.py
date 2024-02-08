from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dtos.UserDTO import UserCreationRequest, UserResponse
from app.services import user_service

user_router = APIRouter(tags=["users"])


@user_router.post("/create/user", status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(user_request: UserCreationRequest, db: Session = Depends(get_db)) -> UserResponse:
    return await user_service.create_user(user_request=user_request, db=db)


@user_router.get("/user/{id}", status_code=HTTPStatus.OK, response_model=UserResponse)
async def get_user_by_id(id: UUID, db: Session = Depends(get_db)) -> UserResponse:
    return await user_service.get_user_by_id(user_id=id, db=db)
