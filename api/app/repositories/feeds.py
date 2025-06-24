import os
import logging

import requests
from app.models import feed as feed_models
from app.repositories import sync as sync_repository
from app.repositories import events as events_repository
from app.repositories import organisations as organisations_repository
from app.schemas import feed as feed_schemas
from app.schemas import user as user_schemas
from app.worker import tasks
from fastapi import HTTPException, status
from pymisp import MISPEvent
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

USER_AGENT = "misp-lite/" + os.environ.get("APP_VERSION", "")


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


def fetch_feed_event_by_uuid(feed, event_uuid):
    url = f"{feed.url}/{event_uuid}.json"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch event {event_uuid}: {response.text}",
        )


def process_feed_event(
    db: Session,
    event_uuid: str,
    feed: feed_models.Feed,
    user: user_schemas.User,
):
    logging.info(f"Fetching event {feed.url}/{event_uuid}")
    event_raw = fetch_feed_event_by_uuid(feed, event_uuid)
    event = MISPEvent()
    event.load(event_raw)

    orgc = organisations_repository.get_or_create_organisation_from_feed(
        db, event.Orgc, user=user
    )

    local_event = events_repository.get_event_by_uuid(db, event_uuid)

    # TODO: process tag_id and tag_collection_id
    # TODO: process feed.sharing_group_id
    # TODO: apply feed rules (disable_correlation, unpublish_event)

    if local_event is None:

        local_event = events_repository.create_event_from_fetched_event(
            db, event, orgc, feed, user
        )

        sync_repository.create_pulled_event_tags(db, local_event, event.tags, user)

        sync_repository.create_pulled_event_reports(
            db, local_event.uuid, event.event_reports, user
        )

        # process objects
        sync_repository.create_pulled_event_objects(
            db, local_event.id, event.objects, user
        )

        # process attributes
        sync_repository.create_pulled_event_attributes(
            db, local_event.id, event.attributes, user
        )
    else:

        local_event = events_repository.update_event_from_fetched_event(
            db, event, orgc, feed, user
        )

        sync_repository.create_pulled_event_tags(db, local_event, event.tags, user)

        sync_repository.create_pulled_event_reports(
            db, local_event.uuid, event.event_reports, user
        )

        # process objects
        sync_repository.update_pulled_event_objects(
            db, local_event.id, event.objects, user
        )

        # process attributes
        sync_repository.update_pulled_event_attributes(
            db, local_event.id, event.attributes, user
        )

    db.commit()

    tasks.index_event.delay(local_event.uuid)

    return {"result": "success", "message": "Event processed"}


def get_feed_manifest(feed: feed_models.Feed):
    return requests.get(f"{feed.url}/manifest.json")


def fetch_feed(db: Session, feed_id: int, user: user_schemas.User):
    logger.info("fetch feed id=%s job started", feed_id)

    db_feed = get_feed_by_id(db, feed_id=feed_id)

    if db_feed is None:
        raise Exception("Feed not found")

    if not db_feed.enabled:
        raise Exception("Feed is not enabled")

    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Feed not found"
        )

    logger.info(f"Fetching feed {db_feed.id} {db_feed.name}")

    if db_feed.source_format == "misp":
        # TODO: check feed etag in redis cache
        req = get_feed_manifest(db_feed)

        if req.status_code == 200:
            manifest = req.json()

            # TODO: cache etag value in redis
            # etag = req.headers.get("etag")
            # logger.info(f"Fetching feed UUID {db_feed.uuid} ETag: {etag}")

            feed_events_uuids = manifest.keys()

            local_feed_events = events_repository.get_events_by_uuids(
                db, feed_events_uuids
            )

            # filter out events that are already in the database and have the same or older timestamp
            skip_events = [
                str(event.uuid)
                for event in local_feed_events
                if event.timestamp >= manifest[str(event.uuid)]["timestamp"]
            ]

            feed_events_uuids = [
                uuid for uuid in feed_events_uuids if uuid not in skip_events
            ]

            # TODO: check if event is blocked by blocklist or feed rules (tags, orgs)

            # fetch events in parallel http requests

            if not feed_events_uuids:
                return {"result": "success", "message": "No new events to fetch"}

            for event_uuid in feed_events_uuids:
                tasks.fetch_feed_event.delay(event_uuid, db_feed.id, user.id)

    logger.info("fetch feed id=%s all event fetch tasks enqueued.", feed_id)
    return {
        "result": "success",
        "message": "All feed id=%s events to fetch enqueued." % feed_id,
    }
