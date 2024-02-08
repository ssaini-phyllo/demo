from sqlalchemy.orm import Session

from app.database.models.models import User


class UserRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id) -> User:
        return self.db_session.query(User).filter(User.id == user_id).first()
