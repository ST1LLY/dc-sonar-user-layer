"""
https://www.django-rest-framework.org/api-guide/views/

Author:
    Konstantin S. (https://github.com/ST1LLY)
"""
# pylint:disable=missing-class-docstring, missing-function-docstring
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import user_cabinet.modules.support_functions as sup_f
from .models import Domain, ReusedPassAcc
from .serializers import (
    DomainSerializer,
    DomainNoExpPassAccSerializer,
    ReusedPassAccSerializer,
    DomainBrutedNTLMAccSerializer,
)


class DomainListCreateAPIView(generics.ListCreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class DomainRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    lookup_field = 'pk'


class DomainBrutedNTLMListAPIView(generics.ListAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainBrutedNTLMAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)


class DomainNoExpPassAccListAPIView(generics.ListAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainNoExpPassAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)


class ReusedPassAccListAPIView(generics.ListAPIView):
    queryset = ReusedPassAcc.objects.all()
    serializer_class = ReusedPassAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('domain',)


class VersionInfo(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        return Response({'version': sup_f.get_file_text(settings.VERSION_FILE_PATH)})
