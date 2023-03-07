# Automatically created by: shub deploy

from setuptools import find_packages, setup

setup(
    name="Artefact News Websites",
    version="1.0",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = news_websites.settings"]},
)
