from django.contrib.auth.models import User
from rest_framework import status, viewsets, generics
from rest_framework.response import Response

from myApp.serializers.user import UserSerializer


class UserDetails(viewsets.ViewSet):
    def create(self, request):
        if request.data:
            user_serializers = UserSerializer(data=request.data)
            user_serializers.is_valid(raise_exception=True)
            user_serializers.save()
            return Response({'message': 'User created successfully', 'status': status.HTTP_201_CREATED,
                             'data': user_serializers.data})

    def list(self, request):
        try:
            query_set = User.objects.filter(is_active=True)
            user_serializer = UserSerializer(query_set, many=True)
            if user_serializer is not None:
                return Response(
                    {'message': 'Users fetched successfully', 'status': status.HTTP_200_OK,
                     'data': user_serializer.data})
            return Response(
                {'message': 'Users not found', 'status': status.HTTP_404_NOT_FOUND, 'data': []})

        except Exception as error:
            return Response(
                {
                    'message': str(error),
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            )


class UserCurd(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # we can even override the generics but best practice is to use viewsets or apiview for customization
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfully", "status": status.HTTP_204_NO_CONTENT},
                        status=status.HTTP_204_NO_CONTENT)
