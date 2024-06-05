from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.orm import relationship

from app.core.db import Base


class AdditionalInfo(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    long_description = Column(Text, unique=True, nullable=False)
    short_description = Column(Text, unique=False, nullable=True)


class Subscription(Base):
    purchase_id = Column(
        ForeignKey('purchase.id', ondelete='CASCADE'),
        primary_key=True
        )
    user_chat_id = Column(
        ForeignKey('user.chat_id', ondelete='CASCADE'),
        primary_key=True
        )


class PurchasePreference(Base):
    purchase_id = Column(
        'purchase_id',
        ForeignKey('purchase.id', ondelete='CASCADE'),
        primary_key=True
        )
    preference_id = Column(
        'preference_id',
        ForeignKey('preference.id', ondelete='CASCADE'),
        primary_key=True
        )


class PurchaseRequirement(Base):
    purchase_id = Column(
        'purchase_id',
        ForeignKey('purchase.id', ondelete='CASCADE'),
        primary_key=True
        )
    requirement_id = Column(
        'requirement_id',
        ForeignKey('requirement.id', ondelete='CASCADE'),
        primary_key=True
        )


class PurchaseRestriction(Base):
    purchase_id = Column(
        'purchase_id',
        ForeignKey('purchase.id', ondelete='CASCADE'),
        primary_key=True
        )
    restriction_id = Column(
        'restriction_id',
        ForeignKey('restriction.id', ondelete='CASCADE'),
        primary_key=True
        )


class Purchase(Base):
    id = Column(Integer, primary_key=True)
    number = Column(String(30), unique=True, nullable=False)
    object_info = Column(Text, unique=False, nullable=False)
    url = Column(String(150), unique=False, nullable=False)
    customer = Column(Text, unique=False, nullable=False)
    end_datetime = Column(DateTime, unique=False, nullable=False)
    price = Column(Float, unique=False, nullable=False)
    is_active = Column(Boolean, default=False)
    subscribers = relationship(
        'User',
        secondary=Subscription.__tablename__,
        back_populates='subscriptions',
        lazy='joined'
    )
    preferences = relationship(
        'Preference',
        secondary=PurchasePreference.__tablename__,
        lazy='joined')
    requirements = relationship(
        'Requirement', secondary=PurchaseRequirement.__tablename__,
        lazy='joined')
    restrictions = relationship(
        'Restriction', secondary=PurchaseRestriction.__tablename__,
        lazy='joined')

    def from_dict(self, data):
        for field in ['number', 'object_info', 'url', 'customer',
                      'end_datetime', 'price']:
            if field in data:
                setattr(self, field, data[field])


class Preference(AdditionalInfo):
    pass


class Requirement(AdditionalInfo):
    pass


class Restriction(AdditionalInfo):
    pass


class InfoMessage(Base):
    id = Column(Integer, primary_key=True)
    info_tomorrow = Column(Boolean, default=False)
    info_today = Column(Boolean, default=False)
