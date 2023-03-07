from config.env import env

MONGODB_CONN = env("MONGODB_CONN")
MONGODB_DATABASE_NAME = env("MONGODB_DATABASE_NAME", default="artefact")
MONGODB_COLLECTION = env("MONGODB_COLLECTION", default="news_articles")
