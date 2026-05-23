from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Items
    
    list: Get all items
    create: Create a new item
    retrieve: Get a specific item
    update: Update an item
    partial_update: Partially update an item
    destroy: Delete an item
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # TBD AELZ: For demo purposes, allow any access. In production, use appropriate permissions.
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        # Only set created_by if user is authenticated
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            # TBD AELZ: For demo purposes, creation only authorized user tbd later
            print("AELZ_501 create an item with ****")
            serializer.save()  # Save without created_by

    def list(self, request, *args, **kwargs):
        print(f"AELZ_504  Query params: {request.data}")
        resp = super().list(request, *args, **kwargs)        
        print(f"AELZ_505  Response data: {resp.data}")
        return  resp

    @action(detail=False, methods=['get'])
    def my_items(self, request):
        """Get items created by the current user: tb when user authenticaiton and authorization is implemented"""
        items = self.queryset
        serializer = self.get_serializer(items, many=True)
        print(f"AELZ_504  Query params: {request.data}")
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle the is_active status of an item"""
        item = self.get_object()
        item.is_active = not item.is_active
        item.save()
        serializer = self.get_serializer(item)
        print("AELZ_503 toggle active ****")
        return Response(serializer.data)
