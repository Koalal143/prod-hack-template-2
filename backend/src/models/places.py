from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    cities: Mapped[list["City"]] = relationship(back_populates="location")


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    location: Mapped["Location"] = relationship(back_populates="cities")
    deliveries: Mapped[list["Delivery"]] = relationship(back_populates="city")