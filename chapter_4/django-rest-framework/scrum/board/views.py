from typing import override
from rest_framework import viewsets
from board.models import Sprint, Task
from board.serializers import SprintSerializer , TaskSerializer, UserSerializer

from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets, filters
from board.models import Sprint
from board.serializers import SprintSerializer

User = get_user_model()

class DefaultsMixin(object):
        """Default settings for view authentication, permissions, filtering and pagination."""
        authentication_classes = (
            authentication.BasicAuthentication,
            authentication.TokenAuthentication,
        )
        permission_classes = (
            permissions.IsAuthenticated,
        )
        paginate_by = 25
        paginate_by_param = 'page_size'
        max_paginate_by = 100
        filter_backends = (
            filters.BaseFilterBackend,
            filters.SearchFilter,
            filters.OrderingFilter,
        )

class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
        """API endpoint for listing and creating sprints."""
        queryset = Sprint.objects.order_by('end')
        serializer_class = SprintSerializer

        # Filters
        search_fields = ['name']
        ordering_fields = ['end', 'name']

        def filter_queryset(self, queryset):
                # Aquí implementas tu lógica personalizada de filtrado
                search = self.request.query_params.get('search', None)
                if search:
                        queryset = queryset.filter(name__icontains=search[0])
                return queryset
class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
        """API endpoint for listing and creating tasks."""
        queryset = Task.objects.all()
        serializer_class = TaskSerializer


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
        """API endpoint for listing users."""
        lookup_field = User.USERNAME_FIELD
        lookup_url_kwarg = User.USERNAME_FIELD
        queryset = User.objects.order_by(User.USERNAME_FIELD)
        serializer_class = UserSerializer
