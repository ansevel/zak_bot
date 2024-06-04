from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey,
                        String, Text)
from sqlalchemy.orm import relationship

from app.core.db import Base


class Subscription(Base):
    purchase_id = Column(
        ForeignKey('purchase.id', ondelete='CASCADE'),
        primary_key=True
        )
    user_id = Column(
        ForeignKey('user.id', ondelete='CASCADE'),
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
        ForeignKey('purchase.id', ondelete='CASCADE')
        )
    requirement_id = Column(
        'requirement_id',
        ForeignKey('requirement.id', ondelete='CASCADE')
        )


class PurchaseRestriction(Base):
    purchase_id = Column(
        'purchase_id',
        ForeignKey('purchase.id', ondelete='CASCADE')
        )
    restriction_id = Column(
        'restriction_id',
        ForeignKey('restriction.id', ondelete='CASCADE')
        )


class Purchase(Base):
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
        back_populates='subscriptions'
    )
    preferences = relationship(
        'Preference', secondary=PurchasePreference.__tablename__)
    requirements = relationship(
        'Requirement', secondary=PurchaseRequirement.__tablename__)
    restrictions = relationship(
        'Restriction', secondary=PurchaseRestriction.__tablename__)


class Preference(Base):
    long_description = Column(Text, unique=True, nullable=False)
    short_description = Column(Text, unique=False, nullable=True)


class Requirement(Base):
    long_description = Column(Text, unique=True, nullable=False)
    short_description = Column(Text, unique=False, nullable=True)


class Restriction(Base):
    dlong_description = Column(Text, unique=True, nullable=False)
    short_description = Column(Text, unique=False, nullable=True)


class InfoMessage(Base):
    info_tomorrow = Column(Boolean, default=False)
    info_today = Column(Boolean, default=False)
