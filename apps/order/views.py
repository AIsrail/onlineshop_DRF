from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from apps.order.models import *


"""test OrderListView """
# class OrderListView(generics. ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated, ]

    # def get_serializer_context(self):
    #     return {'request': self.request}

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

"""test end """

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)