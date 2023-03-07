from django.urls import include, path

urlpatterns = [
    path("articles", include(("artefact.articles.urls", "articles"))),
]
