from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base



class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(primary_key=True)
    days_duration_min: Mapped[int]
    days_duration_max: Mapped[int]

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))

    city: Mapped["City"] = relationship(back_populates="deliveries")
    company: Mapped["Company"] = relationship(back_populates="deliveries")
    tariff: Mapped["Tariff"] = relationship(back_populates="deliveries")
    prices: Mapped[list["Price"]] = relationship(back_populates="delivery")


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float]
    weight: Mapped[int]

    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.id"))

    delivery: Mapped["Delivery"] = relationship(back_populates="prices")


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    deliveries: Mapped[list["Delivery"]] = relationship(back_populates="company")


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    deliveries: Mapped[list["Delivery"]] = relationship(back_populates="tariff")