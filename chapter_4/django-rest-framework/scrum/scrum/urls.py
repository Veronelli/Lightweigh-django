from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from board.url import router

urlpatterns = [
    re_path(r'^api/token/', view=obtain_auth_token, name="api-token"),
    re_path(r'^api/', include(router.urls)),
]
