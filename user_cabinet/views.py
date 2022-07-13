from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Domain, BrutedNTLMAcc, NoExpPassAcc, ReusedPassAcc
from .serializers import (
    DomainSerializer,
    DomainNoExpPassAccSerializer,
    DomainReusedPassAccSerializer,
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


class DomainReusedPassAccListAPIView(generics.ListAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainReusedPassAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)


class VersionInfo(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        return Response({'version': '2022.6.30'})
