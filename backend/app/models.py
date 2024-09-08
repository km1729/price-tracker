# SqlAlchemy models for database
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine, SessionLocal
from datetime import datetime


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String, index=True)
    product_name = Column(String, index=True)
    product_id = Column(String, index=True)
    supplier = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    prices = relationship("Price", back_populates="product")

class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    updated_on = Column(DateTime, default=datetime.now)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="prices")


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)