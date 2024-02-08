import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    email = Column(String, unique=True)
    name = Column(String)
    mobile = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Event(Base):
    __tablename__ = 'events'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


Base.metadata.create_all(engine)
