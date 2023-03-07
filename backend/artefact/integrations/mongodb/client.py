from functools import lru_cache

import pymongo
from artefact.common.utils import assert_settings
from attr import define


@define
class MongoDbConfig:
    conn: str
    database_name: str
    collection: str


@lru_cache
def pymongo_get_configs() -> MongoDbConfig:
    required_config = assert_settings(
        [
            "MONGODB_CONN",
            "MONGODB_DATABASE_NAME",
            "MONGODB_COLLECTION",
        ],
        "MongoDB configs not found.",
    )

    return MongoDbConfig(
        required_config["MONGODB_CONN"],
        required_config["MONGODB_DATABASE_NAME"],
        required_config["MONGODB_COLLECTION"],
    )


def pymongo_get_client():
    config = pymongo_get_configs()
    return pymongo.MongoClient(config.conn)
