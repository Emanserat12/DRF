from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from myApp.models import Order
from myApp.serializers.order import OrderSerializer


class OrderDetails(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        orders_qs = Order.objects.filter(is_removed=False)
        order_serializers = OrderSerializer(orders_qs, many=True)
        return Response({'message': 'Orders fetched Successfully', 'orderDetails': order_serializers.data,
                         'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        order = Order.objects.filter(orderId=pk, is_removed=False).first()
        if not order:
            return Response({'message': 'Order with given Id not Found', 'orderDetails': [],
                             'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        order_serializers = OrderSerializer(order)
        return Response({'message': 'Order Retrieved Successfully', 'orderDetails': order_serializers.data,
                         'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        if request.data:
            order_serializers = OrderSerializer(data=request.data)
            order_serializers.is_valid(raise_exception=True)
            order_serializers.save()
            return Response({'message': 'Order Placed Successfully', 'orderDetails': order_serializers.data,
                             'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None, ):
        order = Order.objects.filter(orderId=pk, is_removed=False).first()
        if not order:
            return Response({'message': 'Order Not Found', 'status': status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
        order.is_removed = True
        order.save()
        return Response({'message': 'Order Cancelled Successfully', 'status': status.HTTP_204_NO_CONTENT},
                        status=status.HTTP_204_NO_CONTENT)
