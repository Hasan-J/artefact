from artefact.integrations.mongodb.client import pymongo_get_client, pymongo_get_configs
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class ArticleListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        url = serializers.CharField()
        author = serializers.CharField()
        title = serializers.CharField()
        body = serializers.ListField(child=serializers.CharField())

        class Meta:
            fields = ("url", "author", "title", "body")

    def get(self, request):
        keyword = request.query_params.get("keyword")

        client = pymongo_get_client()
        config = pymongo_get_configs()

        db = client[config.database_name]
        collection = db[config.collection]

        if keyword is None:
            # handle case where keyword is not provided
            result = collection.find()
        else:
            # handle case where keyword is provided
            result = collection.find({"$text": {"$search": keyword}})

        serializer = self.OutputSerializer(result, many=True)
        return Response(serializer.data)
