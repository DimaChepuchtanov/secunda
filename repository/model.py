from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Integer, String, DateTime,
    ForeignKey, Column, Float
)


Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, index=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())

    address = relationship(
        "Address",
        back_populates="organizations",
        uselist=False
    )
    activity = relationship(
        "Activity",
        back_populates="organizations",
        uselist=False
    )

    def dict(self):
        return {
            "name": self.name,
            "phone": [phone for phone in self.phone.split(";")],
            "address": self.address if self.address else "",
            "created_at": self.created_at
        }


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    street = Column(String(200))
    house_number = Column(String(20))
    apartment = Column(String(20))

    latitude = Column(Float)
    longitude = Column(Float)

    organizations = relationship(
        "Organization",
        back_populates="address"
    )

    def dict(self):
        return {
            "organization_id": self.organization_id,
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            "apartment": self.apartment,
            "geo": f"{self.latitude} x {self.longitude}"
        }


class Activity(Base):
    __tablename__ = "activites"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('activites.id'))

    children = relationship(
        "Activity",
        back_populates="parent",
        lazy="dynamic"
    )

    parent = relationship(
        "Activity",
        back_populates="children",
        remote_side=[id])

    organizations = relationship(
        "Organization",
        back_populates="activity"
    )
