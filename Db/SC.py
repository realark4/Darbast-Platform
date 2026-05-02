from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Db.Dbase import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(String, nullable=True)

    advertisements = relationship("Adver", back_populates="owner", cascade="all, delete-orphan")
    favourites = relationship("Favourites", back_populates="user", cascade="all, delete-orphan")


class Adver(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False, default="sell")  # خرید، فروش، رهن، اجاره
    category_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="advertisements")
    favourites = relationship("Favourites", back_populates="advertisement", cascade="all, delete-orphan")
    images = relationship("AdverImage", back_populates="adver", cascade="all, delete-orphan")


class AdverImage(Base):
    __tablename__ = "adver_images"

    id = Column(Integer, primary_key=True, index=True)
    adver_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)

    adver = relationship("Adver", back_populates="images")


class Favourites(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)

    user = relationship("User", back_populates="favourites")
    advertisement = relationship("Adver", back_populates="favourites")