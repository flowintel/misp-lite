import logging
import time
from datetime import datetime

import requests
from app.models import attribute as attribute_models
from app.models import event as event_models
from app.models import feed as feed_models
from app.models import object as object_models
from app.models import object_reference as object_reference_models
from app.models import organisation as organisation_models
from app.repositories import events as events_repository
from app.repositories import organisations as organisations_repository
from app.schemas import event as event_schemas
from app.schemas import feed as feed_schemas
from app.schemas import user as user_schemas
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(feed_models.Feed).offset(skip).limit(limit).all()


def get_feed_by_id(db: Session, feed_id: int) -> feed_models.Feed:
    return db.query(feed_models.Feed).filter(feed_models.Feed.id == feed_id).first()


def create_feed(db: Session, feed: feed_schemas.FeedCreate):
    db_feed = feed_models.Feed(
        name=feed.name,
        provider=feed.provider,
        url=feed.url,
        rules=feed.rules,
        enabled=feed.enabled,
        distribution=feed.distribution,
        sharing_group_id=feed.sharing_group_id,
        tag_id=feed.tag_id,
        default=feed.default,
        source_format=feed.source_format,
        fixed_event=feed.fixed_event,
        delta_merge=feed.delta_merge,
        event_id=feed.event_id,
        publish=feed.publish,
        override_ids=feed.override_ids,
        settings=feed.settings,
        input_source=feed.input_source,
        delete_local_file=feed.delete_local_file,
        lookup_visible=feed.lookup_visible,
        headers=feed.headers,
        caching_enabled=feed.caching_enabled,
        force_to_ids=feed.force_to_ids,
        orgc_id=feed.orgc_id,
        tag_collection_id=feed.tag_collection_id,
        cached_elements=feed.cached_elements,
        coverage_by_other_feeds=feed.coverage_by_other_feeds,
    )

    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)

    return db_feed


def update_feed(
    db: Session,
    feed_id: int,
    feed: feed_schemas.FeedUpdate,
) -> feed_models.Feed:
    db_feed = get_feed_by_id(db, feed_id=feed_id)

    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Feed not found"
        )

    feed_patch = feed.model_dump(exclude_unset=True)
    for key, value in feed_patch.items():
        setattr(db_feed, key, value)

    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)

    return db_feed


def delete_feed(db: Session, feed_id: int) -> None:
    db_feed = get_feed_by_id(db, feed_id=feed_id)

    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Feed not found"
        )

    db.delete(db_feed)
    db.commit()


def fetch_feed(db: Session, feed_id: int, user: user_schemas.User):
    db_feed = get_feed_by_id(db, feed_id=feed_id)
    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Feed not found"
        )
    logger.info(f"Fetching feed {db_feed.id} {db_feed.name}")

    if db_feed.source_format == "misp":
        # TODO: check feed etag in redis cache
        req = requests.get(f"{db_feed.url}/manifest.json")

        if req.status_code == 200:
            req.json()

            # TODO: cache etag value in redis
            req.headers.get("etag")

            # feed_events_uuids = manifest.keys()
            # local_feed_events = (
            #     db.query(event_models.Event)
            #     .filter(event_models.Event.uuid.in_(feed_events_uuids))
            #     .all()
            # )
            # local_feed_events_uuids = [event.uuid for event in local_feed_events]

            # # filter out events that are already in the database and have the same timestamp
            # skip_events = [
            #     str(event.uuid)
            #     for event in local_feed_events
            #     if event.timestamp == manifest[str(event.uuid)]["timestamp"]
            # ]
            # feed_events_uuids = [
            #     uuid for uuid in feed_events_uuids if uuid not in skip_events
            # ]

            feed_events_uuids = ["5742ea44-5ff4-4634-99c9-4b32950d210f"]
            local_feed_events_uuids = []

            for event_uuid in feed_events_uuids:

                # TODO: check if event is blocked by blocklist or feed rules (tags, orgs)

                if event_uuid in local_feed_events_uuids:
                    # update event
                    pass
                else:
                    # create event

                    # fetch event data
                    event_req = requests.get(f"{db_feed.url}/{event_uuid}.json")

                    if event_req.status_code == 200:
                        event_data = event_req.json()

                        # TODO: if remote event has no distribution set everything to inherit

                        # TODO: process tag_id and tag_collection_id

                        # TODO: process sharing_group_id

                        # TODO: apply feed rules (disable_correlation, unpublish_event)

                        orgc = organisations_repository.get_organisation_by_uuid(
                            db, organisation_uuid=event_data["Event"]["Orgc"]["uuid"]
                        )

                        if orgc is None:
                            logger.info(
                                f"Creating Organisation {event_data['Event']['Orgc']['name']} ({event_data['Event']['Orgc']['uuid']})"
                            )
                            orgc = organisation_models.Organisation(
                                uuid=event_data["Event"]["Orgc"]["uuid"],
                                name=event_data["Event"]["Orgc"]["name"],
                                date_created=datetime.now(),
                                date_modified=datetime.now(),
                                created_by=user.id,
                                local=False,
                            )
                            db.add(orgc)
                            db.commit()
                            db.flush()
                            db.refresh(orgc)

                        db_event = event_models.Event(
                            uuid=event_data["Event"]["uuid"],
                            date=event_data["Event"]["date"],
                            info=event_data["Event"]["info"],
                            user_id=user.id,
                            published=event_data["Event"]["published"],
                            analysis=(
                                event_models.AnalysisLevel(
                                    int(event_data["Event"]["analysis"])
                                )
                                if "analysis" in event_data["Event"]
                                else None
                            ),
                            org_id=user.org_id,
                            orgc_id=orgc.id,
                            timestamp=event_data["Event"]["timestamp"],
                            distribution=(
                                event_schemas.DistributionLevel(
                                    int(event_data["Event"]["distribution"])
                                )
                                if "distribution" in event_data["Event"]
                                else event_schemas.DistributionLevel.ORGANISATION_ONLY
                            ),
                            sharing_group_id=(
                                event_data["Event"]["sharing_group_id"]
                                if "sharing_group_id" in event_data["Event"]
                                else None
                            ),
                            proposal_email_lock=(
                                event_data["Event"]["proposal_email_lock"]
                                if "proposal_email_lock" in event_data["Event"]
                                else False
                            ),
                            locked=(
                                event_data["Event"]["locked"]
                                if "locked" in event_data["Event"]
                                else False
                            ),
                            threat_level=(
                                event_models.ThreatLevel(
                                    int(event_data["Event"]["threat_level_id"])
                                )
                                if "threat_level_id" in event_data["Event"]
                                else None
                            ),
                            publish_timestamp=(
                                event_data["Event"]["publish_timestamp"]
                                if "publish_timestamp" in event_data["Event"]
                                else None
                            ),
                            sighting_timestamp=(
                                event_data["Event"]["sighting_timestamp"]
                                if "sighting_timestamp" in event_data["Event"]
                                else None
                            ),
                            disable_correlation=(
                                event_data["Event"]["disable_correlation"]
                                if "disable_correlation" in event_data["Event"]
                                else False
                            ),
                            extends_uuid=(
                                event_data["Event"]["extends_uuid"]
                                if "extends_uuid" in event_data["Event"]
                                and event_data["Event"]["extends_uuid"] != ""
                                else None
                            ),
                            protected=(
                                event_data["Event"]["protected"]
                                if "protected" in event_data["Event"]
                                else False
                            ),
                            deleted=(
                                event_data["Event"]["deleted"]
                                if "deleted" in event_data["Event"]
                                else False
                            ),
                        )

                        db.add(db_event)
                        db.commit()
                        db.flush()
                        db.refresh(db_event)

                        # process attributes
                        attribute_count = 0
                        if "Attribute" in event_data["Event"]:
                            for attribute in event_data["Event"]["Attribute"]:
                                # TODO: process sharing group
                                # TODO: process tags

                                db_attribute = attribute_models.Attribute(
                                    uuid=attribute["uuid"],
                                    event_id=db_event.id,
                                    type=attribute["type"],
                                    category=attribute["category"],
                                    to_ids=(
                                        attribute["to_ids"]
                                        if "to_ids" in attribute
                                        else False
                                    ),
                                    distribution=event_schemas.DistributionLevel.INHERIT_EVENT,
                                    comment=attribute["comment"],
                                    value=attribute["value"],
                                    timestamp=int(attribute["timestamp"]),
                                    sharing_group_id=(
                                        attribute["sharing_group_id"]
                                        if "sharing_group_id" in attribute
                                        else None
                                    ),
                                    disable_correlation=(
                                        attribute["disable_correlation"]
                                        if "disable_correlation" in attribute
                                        else False
                                    ),
                                    object_id=(
                                        attribute["object_id"]
                                        if "object_id" in attribute
                                        else None
                                    ),
                                    deleted=(
                                        attribute["deleted"]
                                        if "deleted" in attribute
                                        else False
                                    ),
                                )

                                db.add(db_attribute)
                                attribute_count += 1

                        # process objects
                        objects_count = 0
                        if "Object" in event_data["Event"]:
                            for object in event_data["Event"]["Object"]:
                                db_object = object_models.Object(
                                    event_id=db_event.id,
                                    name=object["name"],
                                    meta_category=object["meta-category"],
                                    description=object["description"],
                                    template_uuid=object["template_uuid"],
                                    template_version=object["template_version"],
                                    uuid=object["uuid"],
                                    timestamp=(
                                        object["timetamp"]
                                        if "timetamp" in object
                                        else time.time()
                                    ),
                                    distribution=event_schemas.DistributionLevel.INHERIT_EVENT,
                                    sharing_group_id=(
                                        object["sharing_group_id"]
                                        if "sharing_group_id" in object
                                        else None
                                    ),
                                    comment=(
                                        object["comment"] if "comment" in object else ""
                                    ),
                                    deleted=(
                                        object["deleted"]
                                        if "deleted" in object
                                        else False
                                    ),
                                    first_seen=(
                                        object["first_seen"]
                                        if "first_seen" in object
                                        else None
                                    ),
                                    last_seen=(
                                        object["last_seen"]
                                        if "last_seen" in object
                                        else None
                                    ),
                                )

                                db.add(db_object)
                                db.commit()
                                db.refresh(db_object)
                                objects_count += 1

                                for attribute in object["Attribute"]:
                                    db_attribute = attribute_models.Attribute(
                                        uuid=attribute["uuid"],
                                        event_id=db_event.id,
                                        object_id=db_object.id,
                                        type=attribute["type"],
                                        category=attribute["category"],
                                        to_ids=(
                                            attribute["to_ids"]
                                            if "to_ids" in attribute
                                            else False
                                        ),
                                        distribution=event_schemas.DistributionLevel.INHERIT_EVENT,
                                        comment=(
                                            attribute["comment"]
                                            if "comment" in attribute
                                            else ""
                                        ),
                                        value=attribute["value"],
                                        timestamp=(
                                            int(attribute["timestamp"])
                                            if "timestamp" in attribute
                                            else time.time()
                                        ),
                                        sharing_group_id=(
                                            attribute["sharing_group_id"]
                                            if "sharing_group_id" in attribute
                                            else None
                                        ),
                                        disable_correlation=(
                                            attribute["disable_correlation"]
                                            if "disable_correlation" in attribute
                                            else False
                                        ),
                                        deleted=(
                                            attribute["deleted"]
                                            if "deleted" in attribute
                                            else False
                                        ),
                                    )
                                    db.add(db_attribute)
                                    attribute_count += 1

                                db.commit()

                        # process object references
                        if "Object" in event_data["Event"]:
                            for object in event_data["Event"]["Object"]:
                                if "ObjectReference" in object:
                                    for object_reference in object["ObjectReference"]:
                                        referenced = (
                                            db.query(object_models.Object)
                                            .filter_by(
                                                uuid=object_reference["referenced_uuid"]
                                            )
                                            .first()
                                        )
                                        db_object_reference = (
                                            object_reference_models.ObjectReference(
                                                uuid=object_reference["uuid"],
                                                event_id=db_event.id,
                                                object_id=db_object.id,
                                                referenced_uuid=object_reference[
                                                    "referenced_uuid"
                                                ],
                                                referenced_id=referenced.id,
                                                relationship_type=object_reference[
                                                    "relationship_type"
                                                ],
                                                timestamp=(
                                                    int(object_reference["timestamp"])
                                                    if "timestamp" in object_reference
                                                    else time.time()
                                                ),
                                                referenced_type=referenced.name,
                                                comment=(
                                                    object_reference["comment"]
                                                    if "comment" in object_reference
                                                    else ""
                                                ),
                                                deleted=(
                                                    object_reference["deleted"]
                                                    if "deleted" in object_reference
                                                    else False
                                                ),
                                            )
                                        )
                                        db.add(db_object_reference)

                        # TODO: process event tags
                        # TODO: process event galaxies
                        # TODO: process event sightings
                        # TODO: process event relationships
                        # TODO: process event shadow_attributes
                        # TODO: process event shadow_objects
                        # TODO: process event reports
                        # TODO: process event analyst data

                        events_repository.increment_attribute_count(
                            db, db_event.id, attribute_count
                        )
                        events_repository.increment_object_count(
                            db, db_event.id, objects_count
                        )
                        db.commit()

                    else:
                        logger.error(f"Failed to fetch event {event_uuid}")

            return feed_events_uuids

    return []
