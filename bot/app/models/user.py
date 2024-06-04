from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.purchase import Subscription


class User(Base):
    chat_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    first_name = Column(String(30), unique=False, nullable=True)
    last_name = Column(String(50), unique=False, nullable=True)
    username = Column(String(30), unique=False, nullable=True)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)
    subscriptions = relationship(
        'Purchase',
        secondary=Subscription.__table__,
        back_populates='subscribers',
    )
