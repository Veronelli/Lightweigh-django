from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    re_path(r'^api/token/', view=obtain_auth_token, name="api-token")
]
