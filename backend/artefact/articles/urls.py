from django.urls import path

from .apis import ArticleListApi

urlpatterns = [path("", ArticleListApi.as_view(), name="list")]
