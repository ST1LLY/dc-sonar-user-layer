from django.urls import path

from . import views

urlpatterns = [
    path('domain/', views.DomainListCreateAPIView.as_view()),
    path('domain/<int:pk>/', views.DomainRetrieveUpdateDestroyAPIView.as_view()),
    path('bruted-ntlm-acc/', views.BrutedNTLMAccListCreateAPIView.as_view()),
    path('bruted-ntlm-acc/<int:pk>/', views.BrutedNTLMAccRetrieveUpdateDestroyAPIView.as_view()),
    path('no-exp-pass-acc/', views.NoExpPassAccListCreateAPIView.as_view()),
    path('no-exp-pass-acc/<int:pk>/', views.NoExpPassAccRetrieveUpdateDestroyAPIView.as_view()),
    path('reused-pass-acc/', views.ReusedPassAccListCreateAPIView.as_view()),
    path('reused-pass-acc/<int:pk>/', views.ReusedPassAccRetrieveUpdateDestroyAPIView.as_view()),
]
