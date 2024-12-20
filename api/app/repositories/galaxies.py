import json
import os
from datetime import datetime

from app.models import event as events_models
from app.models import galaxy as galaxies_models
from app.repositories import tags as tags_repository
from app.schemas import galaxy as galaxies_schemas
from app.schemas import user as users_schemas
from fastapi import HTTPException, Query, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session


def get_galaxies(db: Session, filter: str = Query(None)) -> galaxies_models.Galaxy:
    query = db.query(galaxies_models.Galaxy)

    if filter:
        query = query.filter(galaxies_models.Galaxy.namespace.ilike(f"%{filter}%"))

    query = query.order_by(galaxies_models.Galaxy.namespace)

    return paginate(
        query,
        additional_data={"query": {"filter": filter}},
    )


def get_galaxy_by_id(db: Session, galaxy_id: int) -> galaxies_models.Galaxy:
    return (
        db.query(galaxies_models.Galaxy)
        .filter(galaxies_models.Galaxy.id == galaxy_id)
        .first()
    )


def update_galaxies(
    db: Session, user: users_schemas.User
) -> list[galaxies_schemas.Galaxy]:
    galaxies = []
    galaxies_dir = "app/submodules/misp-galaxy/galaxies"
    galaxies_clusters_dir = "app/submodules/misp-galaxy/clusters"

    for root, __, files in os.walk(galaxies_dir):
        for galaxy_file in files:
            if not galaxy_file.endswith(".json"):
                continue

            with open(os.path.join(root, galaxy_file)) as f:
                galaxy_data = json.load(f)
                galaxy = galaxies_models.Galaxy(
                    name=galaxy_data["name"],
                    uuid=galaxy_data["uuid"],
                    namespace=(
                        galaxy_data["namespace"]
                        if "namespace" in galaxy_data
                        else "missing-namespace"
                    ),
                    version=galaxy_data["version"],
                    description=galaxy_data["description"],
                    icon=galaxy_data["icon"],
                    type=galaxy_data["type"],
                    kill_chain_order=(
                        galaxy_data["kill_chain_order"]
                        if "kill_chain_order" in galaxy_data
                        else None
                    ),
                    org_id=user.org_id,
                    orgc_id=user.org_id,
                    created=datetime.now(),
                    modified=datetime.now(),
                )
                db.add(galaxy)
                db.commit()
                db.refresh(galaxy)

                # parse galaxy clusters file
                with open(os.path.join(galaxies_clusters_dir, galaxy_file)) as f:
                    clusters_data_raw = json.load(f)

                    if "values" in clusters_data_raw:
                        for cluster in clusters_data_raw["values"]:
                            galaxy_cluster = galaxies_models.GalaxyCluster(
                                galaxy_id=galaxy.id,
                                uuid=cluster["uuid"],
                                value=cluster["value"],
                                type=(
                                    clusters_data_raw["type"]
                                    if "type" in clusters_data_raw
                                    else galaxy.type
                                ),
                                description=(
                                    cluster["description"]
                                    if "description" in cluster
                                    else ""
                                ),
                                source=(
                                    clusters_data_raw["source"]
                                    if "source" in clusters_data_raw
                                    else None
                                ),
                                version=clusters_data_raw["version"],
                                authors=(
                                    clusters_data_raw["authors"]
                                    if "authors" in clusters_data_raw
                                    else None
                                ),
                                tag_name=f"misp-galaxy:{galaxy.type}={cluster['uuid']}",
                                org_id=user.org_id,
                                orgc_id=user.org_id,
                                collection_uuid=(
                                    clusters_data_raw["collection_uuid"]
                                    if "collection_uuid" in clusters_data_raw
                                    else None
                                ),
                                extends_uuid=(
                                    clusters_data_raw["extends_uuid"]
                                    if "extends_uuid" in clusters_data_raw
                                    else None
                                ),
                                extends_version=(
                                    clusters_data_raw["extends_version"]
                                    if "extends_version" in clusters_data_raw
                                    else None
                                ),
                            )
                            db.add(galaxy_cluster)
                            db.flush()

                            # add galaxy elements
                            if "meta" in cluster:
                                for element in cluster["meta"]:
                                    galaxy_element = galaxies_models.GalaxyElement(
                                        galaxy_cluster_id=galaxy_cluster.id,
                                        key=element,
                                        value=(
                                            cluster["meta"][element]
                                            if isinstance(cluster["meta"][element], str)
                                            else json.dumps(cluster["meta"][element])
                                        ),
                                    )
                                    db.add(galaxy_element)

                            # commit galaxy elements
                            db.commit()

                            # add galaxy relations
                            if "related" in cluster:
                                for relation in cluster["related"]:

                                    # check if valid uuid
                                    if (
                                        "dest-uuid" not in relation
                                        or not relation["dest-uuid"]
                                    ):
                                        continue

                                    galaxy_relation = galaxies_models.GalaxyClusterRelation(
                                        galaxy_cluster_id=galaxy_cluster.id,
                                        galaxy_cluster_uuid=cluster["uuid"],
                                        referenced_galaxy_cluster_uuid=relation[
                                            "dest-uuid"
                                        ],
                                        referenced_galaxy_cluster_type=relation["type"],
                                        default=True,
                                        distribution=events_models.DistributionLevel.ALL_COMMUNITIES,
                                    )
                                    db.add(galaxy_relation)
                                    db.flush()

                                    if "tags" in relation:
                                        for tag in relation["tags"]:
                                            tag = tags_repository.get_tag_by_name(
                                                db, tag_name=tag
                                            )

                                            if tag:
                                                galaxy_relation_tag = galaxies_models.GalaxyClusterRelationTag(
                                                    galaxy_cluster_relation_id=galaxy_relation.id,
                                                    tag=tag,
                                                )

                                                db.add(galaxy_relation_tag)

                            # commit galaxy relations and tags
                            db.commit()

                        # commit galaxy clusters
                        db.commit()

                galaxies.append(galaxy)

    # fix galaxy cluster relations references to galaxy clusters
    relations = db.query(galaxies_models.GalaxyClusterRelation).all()
    for relation in relations:
        galaxy_cluster = (
            db.query(galaxies_models.GalaxyCluster)
            .filter(
                galaxies_models.GalaxyCluster.uuid
                == relation.referenced_galaxy_cluster_uuid
            )
            .first()
        )
        relation.referenced_galaxy_cluster_id = galaxy_cluster.id
        db.add(relation)
    db.commit()

    return galaxies


def update_galaxy(
    db: Session,
    galaxy_id: int,
    galaxy: galaxies_schemas.GalaxyUpdate,
) -> galaxies_models.Galaxy:
    db_galaxy = get_galaxy_by_id(db, galaxy_id=galaxy_id)

    if db_galaxy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Galaxy not found"
        )

    galaxy_patch = galaxy.model_dump(exclude_unset=True)
    for key, value in galaxy_patch.items():
        setattr(db_galaxy, key, value)

    db.add(db_galaxy)
    db.commit()
    db.refresh(db_galaxy)

    return db_galaxy
