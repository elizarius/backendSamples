from rest_framework import viewsets
from .models import SchedulerRegistry
from .serializers import SchedulerRegistrySerializer
from esmlib import utils
from esmlib.filters import CaseInsensitiveOrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

import logging

logger = logging.getLogger('scheduler_registry')


class SchedulerRegistryFilter(FilterSet):
    class Meta:
        model = SchedulerRegistry
        fields = {
            'frequency': ['exact', 'isnull'],
            'endpoint_uri': ['exact', 'contains'],
            'endpoint_data': ['exact', 'contains'],
            'service_metadata': ['exact', 'contains'],
            'is_expired': ['exact'],
            'next_execution_at': ['lte']
        }


class SchedulerRegistryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows creating task schedules
    to be edited or viewed
    """
    # Todo: Create a policy thats enforces only
    # Todo: internal container calls towards TaskScheduler
    queryset = SchedulerRegistry.objects.all()
    serializer_class = SchedulerRegistrySerializer
    filter_backends = (CaseInsensitiveOrderingFilter,
                       DjangoFilterBackend,)
    filter_class = SchedulerRegistryFilter
    ordering = ('next_execution_at')

    auth_policy_group = 'scheduler-registry'

    def destroy(self, request, pk=None):
        try:
            logger.info("AELZ_31 in destroy  req:  {}".format(request.META))
            zz = super(SchedulerRegistryViewSet, self).destroy(request, pk)
            logger.info("AELZ_32 destroy response:  {}".format(zz.status_code))
        except:
            logger.exception(" AELZ_33 in exc {}".format(pk))

        return zz


    def perform_create(self, serializer):
        username = utils.get_username_from_request(self.request)
        serializer.save(service_user=username)

    def get_queryset(self):
        # When we perform update or delete,
        # the queryset is first filtered by username
        username = utils.get_username_from_request(self.request)
        return self.queryset.filter(service_user=username)
