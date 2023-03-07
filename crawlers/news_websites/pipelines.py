# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime

import pymongo

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MongoDBPipeline:
    """Item Pipeline to write data to MongoDB.

    Args:
        mongo_uri (str): The MongoDB connection URI
        mongo_db (str): The name of the MongoDB database
        mongo_coll (str): The name of the MongoDB collection
    """

    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        """Create a pipeline instance from a Crawler.
        A Crawler object provides access to all Scrapy core components
        like settings.
        This method must return a new instance of the pipeline.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_CONN"),
            mongo_db=crawler.settings.get("MONGODB_DATABASE_NAME"),
            mongo_coll=crawler.settings.get("MONGODB_COLLECTION"),
        )

    def open_spider(self, spider):
        """Connect to MongoDB when the spider is opened."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

        # Create a text index to support keyword searching later on
        self.collection.create_index([("title", "text"), ("body", "text")])

    def close_spider(self, spider):
        """Close the connection to MongoDB when the spider is closed."""
        self.client.close()

    def process_item(self, item, spider):
        """Process the items one by one.
        Implementation deals with unique articles and does not created duplicates
        in the target collection when it is ran multiple times.
        """
        item_dict = ItemAdapter(item).asdict()
        self.collection.update_one(
            {"url": item["url"]},
            {"$setOnInsert": item_dict},
            upsert=True,
        )
        return item
