from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    addresses = relationship("Address", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    phone = Column(String)
    full_address = Column(Text)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="addresses")

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    sku = Column(String, index=True)
    title = Column(String)
    last_in_stock = Column(Boolean, default=False)
    last_price = Column(Numeric, default=0)
    last_checked_at = Column(DateTime, nullable=True)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")

class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"))
    event_type = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
