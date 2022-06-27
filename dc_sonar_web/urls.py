"""dc_sonar_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import URLResolver, URLPattern
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView

# list[URLPattern | URLResolver]
# https://github.com/typeddjango/django-stubs/issues/550
urlpatterns: list[URLPattern | URLResolver] = [
    path('admin/', admin.site.urls),
    path('api/user-cabinet/', include('user_cabinet.urls')),
]

urlpatterns += [
    re_path(
        r'(?P<path>.*)',
        TemplateView.as_view(template_name='home.html'),
        name='home',
    )
]
