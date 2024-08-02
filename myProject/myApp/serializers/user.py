from django.contrib.auth.models import User
from rest_framework import serializers, status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError({
                'message': 'User already exists, please login',
                'status': status.HTTP_400_BAD_REQUEST,
                'data': []
            })
        user = User.objects.create_user(**validated_data)
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data['username'] if validated_data.get(
            'username') != instance.username else instance.username
        if validated_data['email'] != instance.email and User.objects.filter(email=validated_data['email']).exclude(
                id=instance.id).exists():
            raise serializers.ValidationError({
                'message': 'Email already exists, please choose a different email',
                'status': status.HTTP_400_BAD_REQUEST
            })

        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data['password'] if validated_data.get(
            'password') != instance.password else instance.password
        if instance.password:
            instance.set_password(instance.password)
            instance.save()
            return instance

    def to_representation(self, instance):
        representation_ = super().to_representation(instance)
        representation_.pop('id')
        representation_['date_joined'] = str(instance.date_joined).split(' ')[0]
        representation_['full_name'] = ' '.join(name.capitalize() for name in instance.username.split('.'))
        return representation_
