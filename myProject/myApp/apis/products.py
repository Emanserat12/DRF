from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from myApp.models import Products
from myApp.serializers.Product import ProductSerializer
from django.shortcuts import get_object_or_404

from signals import product_fetched


class ProductClass(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                query_set = Products.objects.filter(id=pk, is_removed=False).first()
                if query_set is not None:
                    serializer_ = ProductSerializer(query_set)
                    return Response(
                        {
                            'message': 'Product Retrieved Successfully',
                            'data': serializer_.data,
                            'status': status.HTTP_200_OK
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'message': 'Product Not Found',
                            'status': status.HTTP_404_NOT_FOUND
                        })
            except Exception as error:
                return Response(
                    {
                        'message': str(error),
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                    }
                )
        else:
            query_set = Products.objects.filter(is_removed=False)
            serializer_ = ProductSerializer(query_set, many=True)
            product_fetched.send(sender=Products, instance=query_set)
            return Response(
                {'message': 'Products Retrieved Successfully', 'data': serializer_.data, 'status': status.HTTP_200_OK},
            )

    def post(self, request):
        if request.data:
            serializer_class = ProductSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                return Response({'message': 'Product Added Successfully', 'data': serializer_class.data,
                                 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED
                                )
            return Response({'message': serializer_class.errors, 'status': status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Request body cannot be empty',
                         'status': status.HTTP_400_BAD_REQUEST}
                        )

    def patch(self, request, pk=None):
        if pk and request.data:
            try:
                product = Products.objects.get(id=pk)
            except Products.DoesNotExist:
                return Response({'message': 'Product not found', 'status': status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'message': 'Product Updated Successfully',
                    'data': serializer.data,
                    'status': status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Request body cannot be empty', 'status': status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            product_queryset = get_object_or_404(Products, id=pk)
            product_queryset.is_removed = True
            product_queryset.save()
            return Response({'message': 'Product Deleted Successfully!', "status": status.HTTP_204_NO_CONTENT},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Please select a product to delete', "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_204_NO_CONTENT)
