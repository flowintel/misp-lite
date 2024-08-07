"""init

Revision ID: c47c81d4fda3
Revises:
Create Date: 2022-05-05 10:38:45.448013

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c47c81d4fda3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("info", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.types.Uuid(as_uuid=True), nullable=True),
        sa.Column("published", sa.Boolean(), nullable=False),
        sa.Column(
            "analysis",
            postgresql.ENUM(
                "INITIAL",
                "ONGOING",
                "COMPLETE",
                name="analysis_level",
            ),
            nullable=False,
        ),
        sa.Column("attribute_count", sa.Integer(), nullable=True),
        sa.Column("object_count", sa.Integer(), nullable=True),
        sa.Column("orgc_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.types.BigInteger(), nullable=False),
        sa.Column(
            "distribution",
            postgresql.ENUM(
                "ORGANISATION_ONLY",
                "COMMUNITY_ONLY",
                "CONNECTED_COMMUNITIES",
                "ALL_COMMUNITIES",
                "SHARING_GROUP",
                "INHERIT_EVENT",
                name="distribution_level",
            ),
            nullable=False,
        ),
        sa.Column("sharing_group_id", sa.Integer(), nullable=True),
        sa.Column("proposal_email_lock", sa.Boolean(), nullable=False),
        sa.Column("locked", sa.Boolean(), nullable=False),
        sa.Column(
            "threat_level",
            postgresql.ENUM(
                "HIGH",
                "MEDIUM",
                "LOW",
                "UNDEFINED",
                name="threat_level",
            ),
            nullable=False,
        ),
        sa.Column("publish_timestamp", sa.Integer(), nullable=False),
        sa.Column("sighting_timestamp", sa.Integer(), nullable=True),
        sa.Column("disable_correlation", sa.Boolean(), nullable=True),
        sa.Column("extends_uuid", sa.types.Uuid(as_uuid=True), nullable=True),
        sa.Column("protected", sa.Boolean(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_index(
        op.f("ix_events_extends_uuid"), "events", ["extends_uuid"], unique=False
    )
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)
    op.create_index(op.f("ix_events_info"), "events", ["info"], unique=False)
    op.create_index(op.f("ix_events_org_id"), "events", ["org_id"], unique=False)
    op.create_index(op.f("ix_events_orgc_id"), "events", ["orgc_id"], unique=False)
    op.create_index(
        op.f("ix_events_sharing_group_id"), "events", ["sharing_group_id"], unique=False
    )
    op.create_table(
        "attributes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("object_id", sa.Integer(), nullable=True),
        sa.Column("object_relation", sa.String(length=255), nullable=True),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column("value", sa.String(), nullable=True),
        sa.Column("to_ids", sa.Boolean(), nullable=True),
        sa.Column("uuid", sa.types.Uuid(as_uuid=True), nullable=True),
        sa.Column("timestamp", sa.types.BigInteger(), nullable=False),
        sa.Column(
            "distribution",
            postgresql.ENUM(name="distribution_level", create_type=False),
            nullable=False,
        ),
        sa.Column("sharing_group_id", sa.Integer(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.Column("disable_correlation", sa.Boolean(), nullable=True),
        sa.Column("first_seen", sa.BigInteger(), nullable=True),
        sa.Column("last_seen", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_index(
        op.f("ix_attributes_category"), "attributes", ["category"], unique=False
    )
    op.create_index(
        op.f("ix_attributes_event_id"), "attributes", ["event_id"], unique=False
    )
    op.create_index(
        op.f("ix_attributes_first_seen"), "attributes", ["first_seen"], unique=False
    )
    op.create_index(op.f("ix_attributes_id"), "attributes", ["id"], unique=False)
    op.create_index(
        op.f("ix_attributes_last_seen"), "attributes", ["last_seen"], unique=False
    )
    op.create_index(
        op.f("ix_attributes_object_id"), "attributes", ["object_id"], unique=False
    )
    op.create_index(
        op.f("ix_attributes_object_relation"),
        "attributes",
        ["object_relation"],
        unique=False,
    )
    op.create_index(
        op.f("ix_attributes_sharing_group_id"),
        "attributes",
        ["sharing_group_id"],
        unique=False,
    )
    op.create_index(op.f("ix_attributes_type"), "attributes", ["type"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_attributes_type"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_sharing_group_id"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_object_relation"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_object_id"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_last_seen"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_id"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_first_seen"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_event_id"), table_name="attributes")
    op.drop_index(op.f("ix_attributes_category"), table_name="attributes")
    op.drop_table("attributes")
    op.drop_index(op.f("ix_events_sharing_group_id"), table_name="events")
    op.drop_index(op.f("ix_events_orgc_id"), table_name="events")
    op.drop_index(op.f("ix_events_org_id"), table_name="events")
    op.drop_index(op.f("ix_events_info"), table_name="events")
    op.drop_index(op.f("ix_events_id"), table_name="events")
    op.drop_index(op.f("ix_events_extends_uuid"), table_name="events")
    op.drop_table("events")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
