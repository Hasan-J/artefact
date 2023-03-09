# conftest.py

import uuid

import pytest
import requests
from django.conf import settings
from pymongo import MongoClient


@pytest.fixture(scope="module")
def mongo_client():
    # Create a MongoClient instance
    client = MongoClient(settings.MONGODB_CONN)
    yield client
    client.close()


@pytest.fixture(scope="class")
def insert_sample_docs(mongo_client):
    # Insert sample documents into the test database
    db = mongo_client[settings.MONGODB_DATABASE_NAME]
    sample_docs = [
        {
            "url": "http://host/articles/1",
            "author": "Author1",
            "body": ["sentence1", "sentence2"],
            "title": "Article1",
        },
        {
            "url": "http://host/articles/2",
            "author": "Author2",
            "body": ["sentence1", "sentence2"],
            "title": "Article2",
        },
        {
            "url": "http://host/articles/3",
            "author": "Author3",
            "body": ["sentence1", "sentence2"],
            "title": "Article3",
        },
        {
            "url": "http://host/articles/4",
            "author": "Author4",
            "body": ["sentence1", "sentence2"],
            "title": "Article4",
        },
    ]
    db[settings.MONGODB_COLLECTION].insert_many(sample_docs)


@pytest.fixture()
def get_sample_docs(request):
    # Retrieve the sample documents from the test database
    url = request.param
    response = requests.get(url)
    return response.json()


@pytest.mark.usefixtures("insert_sample_docs")
class TestArticleListApi:
    @pytest.mark.parametrize(
        ("get_sample_docs, expected_items_returned"),
        [("http://backend:8000/api/articles", 4)],
        indirect=["get_sample_docs"],
    )
    def test_get(self, get_sample_docs, expected_items_returned):
        # Test if the retrieved sample documents have the expected keys
        for doc in get_sample_docs:
            assert "url" in doc.keys()
            assert "author" in doc.keys()
            assert "body" in doc.keys()
            assert "title" in doc.keys()

        # Check that the length of get_sample_docs is as expected
        assert len(get_sample_docs) == expected_items_returned
