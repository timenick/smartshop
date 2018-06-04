# Stdlib imports
# Core Django imports
from django.http import Http404
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from .models import Tag
from .serializers import TagSerializer, TagQueryResponseSerializer
from merchandises.models import Merchandise
from merchandises.serializers import MerchandiseListShowInfoSerializer


class TagCreateView(APIView):
    """
    Create a new tag, used when do in-stock
    """
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDeleteView(DestroyAPIView):
    """
    Delete a tag from database
    """
    def get_object(self, pk):
        try:
            return Tag.objects.get(EPC=pk)
        except Tag.DoesNotExist:
            raise Http404

    def delete(self, request):
        epc = request.data.get('EPC')
        tag = self.get_object(epc)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagQueryView(APIView):
    """
    Query a list of merchandise ID by tag EPCs
    and send back the merchandises information
    """
    def post(self, request):
        taglist = request.data
        li = taglist.getlist('EPC')
        tags = Tag.objects.filter(EPC__in=li)
        ids = tags.values_list('merchandiseID')
        merchandises = Merchandise.objects.filter(pk__in=ids)
        output_serializer = MerchandiseListShowInfoSerializer(merchandises, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
