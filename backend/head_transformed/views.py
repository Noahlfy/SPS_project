from rest_framework import viewsets

from head_transformed.models import HeadTransformed

from head_transformed.serializers import HeadTransformedSerializer


class HeadTransformedViewSet(viewsets.ModelViewSet):
    queryset = HeadTransformed.objects.all()
    serializer_class = HeadTransformedSerializer