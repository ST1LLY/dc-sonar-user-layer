"""
The views of the project
"""
from typing import Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):   # pylint: disable=W0223
    """
    Customizing token claims
    https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
    """

    @classmethod
    def get_token(cls, user: Any) -> Any:
        # noinspection PyUnresolvedReferences
        token = super().get_token(user)

        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Customizing token claims
    https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
    """

    serializer_class = MyTokenObtainPairSerializer
