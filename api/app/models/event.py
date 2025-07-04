import enum
import uuid

from app.database import Base
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DistributionLevel(enum.Enum):
    """
    Enum for the Event distribution level
    """

    ORGANISATION_ONLY = 0
    COMMUNITY_ONLY = 1
    CONNECTED_COMMUNITIES = 2
    ALL_COMMUNITIES = 3
    SHARING_GROUP = 4
    INHERIT_EVENT = 5


class ThreatLevel(enum.Enum):
    """
    Enum for the Event threat level
    """

    HIGH = 1
    MEDIUM = 2
    LOW = 3
    UNDEFINED = 4


class AnalysisLevel(enum.Enum):
    """
    Enum for the Event analysis level
    """

    INITIAL = 0
    ONGOING = 1
    COMPLETE = 2


class Event(Base):
    __tablename__ = "events"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    org_id = Column(Integer, ForeignKey("organisations.id"), index=True, nullable=False)
    date = Column(Date, nullable=False)
    info = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    published = Column(Boolean, default=False, nullable=False)
    analysis: Mapped[AnalysisLevel] = mapped_column(
        Enum(AnalysisLevel, name="analysis_level"),
        nullable=False,
        default=AnalysisLevel.INITIAL,
    )
    attribute_count = Column(Integer, default=0)
    object_count = Column(Integer, default=0)
    orgc_id = Column(
        Integer, ForeignKey("organisations.id"), index=True, nullable=False
    )
    timestamp = Column(Integer, nullable=False, default=0)
    distribution: Mapped[DistributionLevel] = mapped_column(
        Enum(DistributionLevel, name="distribution_level"),
        nullable=False,
        default=DistributionLevel.ORGANISATION_ONLY,
    )
    sharing_group_id = Column(
        Integer, ForeignKey("sharing_groups.id"), index=True, nullable=True
    )
    proposal_email_lock = Column(Boolean, nullable=False, default=False)
    locked = Column(Boolean, nullable=False, default=False)
    threat_level: Mapped[ThreatLevel] = mapped_column(
        Enum(ThreatLevel, name="threat_level"),
        nullable=False,
        default=ThreatLevel.UNDEFINED,
    )
    publish_timestamp = Column(Integer, nullable=False, default=0)
    sighting_timestamp = Column(Integer, nullable=True)
    disable_correlation = Column(Boolean, default=False)
    extends_uuid = Column(UUID(as_uuid=True), index=True, nullable=True)
    protected = Column(Boolean, nullable=False, default=False)
    deleted = Column(Boolean, nullable=False, default=False)

    attributes = relationship("Attribute", lazy="subquery", cascade="all, delete-orphan")
    objects = relationship("Object", lazy="subquery", cascade="all, delete-orphan")
    sharing_group = relationship("SharingGroup", lazy="joined")
    tags = relationship("Tag", secondary="event_tags", lazy="joined")
