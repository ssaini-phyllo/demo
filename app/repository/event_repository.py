from sqlalchemy.orm import Session

from app.database.models.models import Event


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update_event(self, event):
        try:
            self.db.commit()
            self.db.refresh(event)
            return event
        except Exception as ex:
            self.db.rollback()
            raise ex

    def get_event_by_id(self, id):
        return self.db.query(Event).filter(Event.id == id).first()

    def get_events_by_user_id(self, user_id):
        return self.db.query(Event).filter(Event.user_id == user_id).all()
