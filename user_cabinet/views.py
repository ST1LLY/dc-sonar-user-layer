from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Domain, BrutedNTLMAcc, NoExpPassAcc, ReusedPassAcc
from .serializers import DomainSerializer, BrutedNTLMAccSerializer, NoExpPassAccSerializer, ReusedPassAccSerializer


class DomainListCreateAPIView(generics.ListCreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class DomainRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    lookup_field = 'pk'


class BrutedNTLMAccListCreateAPIView(generics.ListCreateAPIView):
    queryset = BrutedNTLMAcc.objects.all()
    serializer_class = BrutedNTLMAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('domain',)


class BrutedNTLMAccRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrutedNTLMAcc.objects.all()
    serializer_class = BrutedNTLMAccSerializer
    lookup_field = 'pk'


class NoExpPassAccListCreateAPIView(generics.ListCreateAPIView):
    queryset = NoExpPassAcc.objects.all()
    serializer_class = NoExpPassAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('domain',)


class NoExpPassAccRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NoExpPassAcc.objects.all()
    serializer_class = NoExpPassAccSerializer
    lookup_field = 'pk'


class ReusedPassAccListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReusedPassAcc.objects.all()
    serializer_class = ReusedPassAccSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('domain',)


class ReusedPassAccRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReusedPassAcc.objects.all()
    serializer_class = ReusedPassAccSerializer
    lookup_field = 'pk'
