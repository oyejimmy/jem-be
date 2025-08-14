from sqlalchemy import Column, Integer, String, Float, Text
from app.database.db import Base
from sqlalchemy.orm import declarative_base

# Base is defined here
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)

class Anklet(Base):
    __tablename__ = "anklets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)

class Bangle(Base):
    __tablename__ = "bangles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class Bracelet(Base):
    __tablename__ = "bracelets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class Combo(Base):
    __tablename__ = "combos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class EarStud(Base):
    __tablename__ = "ear_studs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class Earing(Base):
    __tablename__ = "earings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class Hoop(Base):
    __tablename__ = "hoops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class Pendant(Base):
    __tablename__ = "pendants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class Ring(Base):
    __tablename__ = "rings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)


class WallFrame(Base):
    __tablename__ = "wall_frames"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    status = Column(String, nullable=True)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
