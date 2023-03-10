# Artefact Assignment

This is an assignment done for Artefact during an interview process.

The code is split into two parts:

- **crawlers**

    Contains Scrapy spiders that crawl and fetch articles from news websites, and inserts them into a MongoDB.

    *Current imlpemented little spiders:*

    | Spider | Website |
    | -------- | -------- |
    | bbc | http://www.bbc.com/news |

- **backend**

    Contains a Django app that exposes a REST API for searching crawled news articles that are stored in a MongoDB.

    *Published endpoint*

    ```html
    GET http://localhost:8000/articles?keyword=<VALUE>
    ```


## Table Of Content

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage - Local](#usage---local)
- [Usage - Docker](#usage---docker)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

Change dir to one of the directories `crawlers` or `backend`, then:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements/{[base|local]}.txt
```

## Configuration

Both can be configured with the same environment variables:

- `MONGODB_CONN` (The MongoDB connection string)
- `MONGODB_DATABASE_NAME` (The name of the MongoDB database, defaults to artefact)
- `MONGODB_COLLECTION` (The name of the MongoDB collection, defaults to news_articles)

### crawlers

Have the env vars exported in the current working shell (on linux use `export` or use local vscode settings, etc...)

### backend

Copy the `backend/.env.example` file into `backend/.env` and put your custom values in it.

## Usage - Local

### crawlers

Run the `bbc` spider that will fetch articles from [BBC](https://www.bbc.com/news).

```bash
# crawl the main /news section
scrapy crawl bbc 

# crawl subsections of /news (e.g. /news/sports, /news/technology)
scrapy crawl bbc -a section=technology
```

### backend

Run the local server:

```bash
python manage.py runserver
```

Call the following endpoint:

```bash
# Get all articles from the database
curl http://localhost:8000/api/articles

# Get articles by keyword (matches are done on the article title and full text)
curl http://localhost:8000/api/articles?keyword=<VALUE>
```

## Usage - Docker

In case you don't want to install enything on your local host, you can run everything in docker.

The main compose file in the repo contains 3 services:

- mongo: MongoDB database.
- crawlers: Runs the container for bbc spider and crawls the news website, it's a one-off command, it will run and exit with code zero when finished.
- backend: will run the django local server.

In the root of repo:
```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up
```

You will see some logs related to crawling, then crawlers container will stop. After that you can start requesting articles using the backend at http://localhost:8000/articles

## Testing

### crawlers

*(ps: you still need an internet connection)*

In order to avoid test cases becoming unwieldy in the future, I opted to stick to the integrated method that scrapy provides, using [scrapy contracts](https://docs.scrapy.org/en/latest/topics/contracts.html).

The spider's contracts should specify reasonable parameters after monitoring their callbacks behavior when ran against their relative website.

We can then check our expectations for them using:

```bash
scrapy check
```

### backend

Currently includes only integration tests that can be executed inside a docker environment.

To run the integration tests, do:

```bash
make tests
```

This will spin up the necessary containers in a separate docker compose project, run the tests and then strip down everything
leaving you with a clean environment.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
