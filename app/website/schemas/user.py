from sqlalchemy import Boolean, Column, String, Time
from app.database import Base
from .base_entity import BaseEntity
from sqlalchemy.orm import relationship
from flask_login import UserMixin    
    
class User(Base, BaseEntity, UserMixin):
    __tablename__ = "users"
    
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Time)
    photo_url = Column(String)
    telephone = Column(String)
    address = Column(String)
    experience_in = Column(String)
    addition_detail = Column(String)
    is_active = Column(Boolean, nullable=False, default = True)
    is_admin = Column(Boolean, nullable=False, default = False)
    ratings = relationship('Rating', back_populates='user', lazy='immediate')
    
    def get_id(self) -> str:
        return str(self.id)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}