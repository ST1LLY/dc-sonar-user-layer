from django.urls import path

from . import views

urlpatterns = [
    path('domain/', views.DomainListCreateAPIView.as_view()),
    path('domain/<int:pk>/', views.DomainRetrieveUpdateDestroyAPIView.as_view()),
    path('domain-bruted-ntlm-acc/', views.DomainBrutedNTLMListAPIView.as_view()),
    path('domain-no-exp-pass-acc/', views.DomainNoExpPassAccListAPIView.as_view()),
    path('domain-reused-pass-acc/', views.ReusedPassAccListAPIView.as_view()),
    path('version/', views.VersionInfo.as_view()),
]
