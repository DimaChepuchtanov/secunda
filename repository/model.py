from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import String, DateTime, Column


Base = declarative_base()


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, index=True)
    text = Column(String)
    status = Column(String, default="created")
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())

    def dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "status": self.status if self.status else "created",
            "author": self.author,
            "created_at": datetime.strftime(self.created_at, "%Y-%m-%d %H:%m:%S") if self.created_at else datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%m:%S")
        }
