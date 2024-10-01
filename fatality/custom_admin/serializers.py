from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


class ServiceSerializer(serializers.ModelSerializer):
    # tasks = serializers.StringRelatedField(many=True, read_only=True)
    # projects = serializers.StringRelatedField(many=True, read_only=True)
    processes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'


class ProcessDevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessDevelopment
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(source='service', queryset=Service.objects.all())
    reviewed = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'phone_number', 'service_id', 'reviewed', 'comment', 'created_at')


class ProjectBlockSerializer(serializers.ModelSerializer):
    block_photos = serializers.StringRelatedField(many=True, required=False)

    # def create(self, validated_data):
    #     project_block = ProjectBlock.objects.create(**validated_data)
    #     if 'block_photos' in validated_data:
    #         photos_data = validated_data.pop('block_photos')
    #         for photo_data in photos_data:
    #             ProjectBlockPhoto.objects.create(block=project_block, **photo_data)
    #     return project_block

    class Meta:
        model = ProjectBlock
        fields = '__all__'


class ProjectBlockPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBlockPhoto
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # service_id = serializers.PrimaryKeyRelatedField(source='service', queryset=Service.objects.all())
    small_photos = serializers.StringRelatedField(many=True, read_only=True)
    big_photos = serializers.StringRelatedField(many=True, read_only=True)
    blocks = ProjectBlockSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        # fields = ('id', 'title', 'description', 'about', 'about_content', 'solution', 'service_id',
        #           'color', 'cover', 'background_1', 'background_2', 'small_photos', 'big_photos', 'index_number')


class SmallPhotoProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(source='project', queryset=Project.objects.all())

    class Meta:
        model = SmallPhotoProject
        fields = ('id', 'title', 'project_id', 'upload', 'index_number')


class BigPhotoProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(source='project', queryset=Project.objects.all())

    class Meta:
        model = BigPhotoProject
        fields = ('id', 'title', 'project_id', 'upload', 'index_number')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'position', 'email', 'avatar',
                  'date_joined', 'is_superuser')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'position', 'avatar')
        extra_kwargs = {'email': {'required': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'],
                                        first_name=validated_data.get('first_name', None),
                                        last_name=validated_data.get('last_name', None),
                                        position=validated_data.get('position', None),
                                        avatar=validated_data.get('avatar', None), )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверный логин или пароль.")


class SiteUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = SiteUser
        fields = '__all__'
