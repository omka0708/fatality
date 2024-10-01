from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .apps import SERVICE_DESCRIPTION
from .models import Post, Task, Service, Project, SmallPhotoProject, User, Review, BigPhotoProject, ProcessDevelopment, \
    SiteUser, ProjectBlock, ProjectBlockPhoto
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, PostSerializer, TaskSerializer, \
    ServiceSerializer, ProjectSerializer, ReviewSerializer, SmallPhotoProjectSerializer, BigPhotoProjectSerializer, \
    ProcessDevelopmentSerializer, SiteUserSerializer, ProjectBlockSerializer, ProjectBlockPhotoSerializer


def base_view(request):
    return render(request, template_name='index.html')


@extend_schema(summary='Прочитать сервисы')
class ServiceReadAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


@extend_schema(summary='Получить сервис')
class ServiceDetailAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


@extend_schema(summary='Добавить сервис (только для суперпользователя)')
class ServiceCreateAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


@extend_schema(summary='Изменить сервис (только для суперпользователя)', description=SERVICE_DESCRIPTION)
class ServiceUpdateAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


@extend_schema(summary='Удалить сервис (только для суперпользователя)', description=SERVICE_DESCRIPTION)
class ServiceDeleteAPI(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


@permission_classes((permissions.IsAdminUser,))
@extend_schema(summary='Удалить photo_present_project у сервиса')
@api_view(['DELETE'])
def service_photo_present_project_delete(request, pk):
    if request.method == "DELETE":
        obj = get_object_or_404(Service, pk=pk)
        if obj.photo_present_project:
            obj.photo_present_project = None
            obj.save()
            return Response(f'photo_present_project у сервиса с id={pk} удалён')
        else:
            return Response(f'photo_present_project у сервиса с id={pk} и так отсутствует')


@extend_schema(summary='Добавить/прочитать процессы', description=SERVICE_DESCRIPTION)
class ProcessDevelopmentListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = ProcessDevelopment.objects.all()
    serializer_class = ProcessDevelopmentSerializer


@extend_schema(summary='Прочитать/изменить/удалить процесс')
class ProcessDevelopmentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = ProcessDevelopment.objects.all()
    serializer_class = ProcessDevelopmentSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='service_id', type=int),
        ]
    )
)
@extend_schema(summary='Добавить заявку', description=SERVICE_DESCRIPTION)
class TaskCreateAPI(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='service_id', type=int),
        ]
    )
)
@extend_schema(summary='Прочитать заявку (только для аутентифицированных)', description=SERVICE_DESCRIPTION)
class TaskListAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        if service_id:
            queryset = Task.objects.filter(service_id=service_id)
        else:
            queryset = Task.objects.all()
        return queryset


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='service_id', type=int),
        ]
    )
)
@extend_schema(summary='Изменить заявку (только для суперпользователя)', description=SERVICE_DESCRIPTION)
class TaskUpdateAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@extend_schema(summary='Удалить заявку (только для суперпользователя)')
class TaskDestroyAPI(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@extend_schema(summary='Рассмотреть заявку/убрать из рассмотренных (чекбокс)')
class TaskReviewAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Task, pk=pk)
        obj.reviewed = not obj.reviewed
        obj.save()
        if obj.reviewed:
            return Response('Заявка рассмотрена')
        else:
            return Response('Заявка убрана из рассмотрения')


@extend_schema(summary='Добавить/прочитать проект', description=SERVICE_DESCRIPTION)
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='service_id', type=int),
        ]
    )
)
class ProjectListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        if service_id:
            queryset = Project.objects.filter(blocks__service=service_id)
        else:
            queryset = Project.objects.all()
        return queryset


@extend_schema(summary='Прочитать/изменить/удалить проект')
class ProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@permission_classes((permissions.IsAuthenticated,))
@extend_schema(summary='Удалить cover у проекта')
@api_view(['DELETE'])
def project_cover_delete(request, pk):
    if request.method == "DELETE":
        obj = get_object_or_404(Project, pk=pk)
        if obj.cover:
            obj.cover = None
            obj.save()
            return Response(f'cover у проекта с id={pk} удалён')
        else:
            return Response(f'cover у проекта с id={pk} и так отсутствует')


@extend_schema(summary='Удалить background_1 у проекта')
@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def project_b1_delete(request, pk):
    if request.method == "DELETE":
        obj = get_object_or_404(Project, pk=pk)
        if obj.background_1:
            obj.background_1 = None
            obj.save()
            return Response(f'background_1 у проекта с id={pk} удалён')
        else:
            return Response(f'background_1 у проекта с id={pk} и так отсутствует')


@extend_schema(summary='Удалить background_2 у проекта')
@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def project_b2_delete(request, pk):
    if request.method == "DELETE":
        obj = get_object_or_404(Project, pk=pk)
        if obj.background_2:
            obj.background_2 = None
            obj.save()
            return Response(f'background_2 у проекта с id={pk} удалён')
        else:
            return Response(f'background_2 у проекта с id={pk} и так отсутствует')


# @extend_schema(summary='Добавить сервис к проекту', description=SERVICE_DESCRIPTION,
#                parameters=[
#                    OpenApiParameter(name='service_id', type=int),
#                ])
# @api_view(['POST'])
# @permission_classes((permissions.IsAuthenticated,))
# def project_add_service(request, pk):
#     if request.method == "POST":
#         project = get_object_or_404(Project, pk=pk)
#         service_id = request.query_params.get('service_id')
#         if service_id:
#             service = get_object_or_404(Service, pk=service_id)
#             if service in project.service.all():
#                 return Response(f'Проект {project.title} уже содержит сервис {service.title}')
#             else:
#                 project.service.add(service)
#                 project.save()
#                 return Response(f'Сервис {service.title} прикреплён к проекту {project.title}')
#         else:
#             return Response('service_id обязателен')
#
#
# @extend_schema(summary='Удалить сервис из проекта', description=SERVICE_DESCRIPTION,
#                parameters=[
#                    OpenApiParameter(name='service_id', type=int),
#                ])
# @api_view(['DELETE'])
# @permission_classes((permissions.IsAuthenticated,))
# def project_delete_service(request, pk):
#     if request.method == "DELETE":
#         project = get_object_or_404(Project, pk=pk)
#         service_id = request.query_params.get('service_id')
#         if service_id:
#             service = get_object_or_404(Service, pk=service_id)
#             if service not in project.service.all():
#                 return Response(f'Сервис с id={service_id} и так отсутствует у проекта {project.title}')
#             else:
#                 project.service.remove(service)
#                 project.save()
#                 return Response(f'Сервис {service.title} удалён из проекта {project.title}')
#         else:
#             return Response('service_id обязателен')

@extend_schema(summary='Добавить/прочитать блоки')
class ProjectBlockListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = ProjectBlock.objects.all()
    serializer_class = ProjectBlockSerializer


@extend_schema(summary='Прочитать/изменить/удалить блок')
class ProjectBlockDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = ProjectBlock.objects.all()
    serializer_class = ProjectBlockSerializer


@extend_schema(summary='Добавить/прочитать фотку блока')
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='block_id', type=int),
        ]
    )
)
class ProjectBlockPhotoListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = ProjectBlockPhoto.objects.all()
    serializer_class = ProjectBlockPhotoSerializer

    def get_queryset(self):
        block_id = self.request.query_params.get('block_id')
        if block_id:
            queryset = ProjectBlockPhoto.objects.filter(block=block_id)
        else:
            queryset = ProjectBlockPhoto.objects.all()
        return queryset


@extend_schema(summary='Прочитать/изменить/удалить фотку блока', )
class ProjectBlockPhotoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = ProjectBlockPhoto.objects.all()
    serializer_class = ProjectBlockPhotoSerializer


@extend_schema(summary='Добавить/прочитать маленькую фотку')
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='project_id', type=int),
        ]
    )
)
class SmallPhotoProjectListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = SmallPhotoProject.objects.all()
    serializer_class = SmallPhotoProjectSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = SmallPhotoProject.objects.filter(project_id=project_id)
        else:
            queryset = SmallPhotoProject.objects.all()
        return queryset


@extend_schema(summary='Прочитать/изменить/удалить маленькую фотку', )
class SmallPhotoProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = SmallPhotoProject.objects.all()
    serializer_class = SmallPhotoProjectSerializer


@extend_schema(summary='Добавить/прочитать большую фотку', )
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='project_id', type=int),
        ]
    )
)
class BigPhotoProjectListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = BigPhotoProject.objects.all()
    serializer_class = BigPhotoProjectSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = BigPhotoProject.objects.filter(project_id=project_id)
        else:
            queryset = BigPhotoProject.objects.all()
        return queryset


@extend_schema(summary='Прочитать/изменить/удалить большую фотку', )
class BigPhotoProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = BigPhotoProject.objects.all()
    serializer_class = BigPhotoProjectSerializer


@extend_schema(summary='Добавить/прочитать посты')
class PostListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(serializer.data)


@extend_schema(summary='Прочитать/изменить/удалить пост')
class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@extend_schema(summary='Добавить/прочитать отзывы')
class ReviewListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


@extend_schema(summary='Прочитать/изменить/удалить отзыв')
class ReviewDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


@extend_schema(summary='Создать пользователя (только для суперпользователя)')
class UserCreateAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAdminUser
    ]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


@extend_schema(summary='Получить пользователя')
class UserDetailAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


@extend_schema(summary='Изменить пользователя по id (только для суперпользователя)')
class UserUpdateAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAdminUser
    ]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


@extend_schema(summary='Удалить пользователя по id (только для суперпользователя)')
class UserDeleteAPI(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAdminUser
    ]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


@extend_schema(summary='Получить всех пользователей')
class UserListAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


@extend_schema(summary='Получить/изменить/удалить текущего пользователя (себя)')
class CurrentUserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
#                          "token": AuthToken.objects.create(user)[1]})


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
                         "token": AuthToken.objects.create(user)[1]})


@extend_schema(summary='Добавить/прочитать пользователей сайта')
class SiteUserListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer


@extend_schema(summary='Прочитать/изменить/удалить пользователя сайта')
class SiteUserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer
