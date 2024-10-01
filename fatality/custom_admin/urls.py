from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import *
from knox import views as knox_views

urlpatterns = ([
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    # path('api/auth/register', RegisterAPI.as_view(), name='register'),
    path('api/auth/login', LoginAPI.as_view(), name='login'),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='logout'),

    path('api/user/add', UserCreateAPI.as_view()),
    path('api/user/<int:pk>', UserDetailAPI.as_view()),
    path('api/user/<int:pk>/update', UserUpdateAPI.as_view()),
    path('api/user/<int:pk>/delete', UserDeleteAPI.as_view()),

    path('api/site_user', SiteUserListAPI.as_view()),
    path('api/site_user/<int:pk>', SiteUserDetailAPI.as_view()),

    path('api/user/all', UserListAPI.as_view()),
    path('api/user/me', CurrentUserDetailAPI.as_view()),

    path('api/blog', PostListAPI.as_view()),
    path('api/blog/<int:pk>', PostDetailAPI.as_view()),

    path('api/service', ServiceReadAPI.as_view()),
    path('api/service/<int:pk>', ServiceDetailAPI.as_view()),
    path('api/service/add', ServiceCreateAPI.as_view()),
    path('api/service/<int:pk>/update', ServiceUpdateAPI.as_view()),
    path('api/service/<int:pk>/delete', ServiceDeleteAPI.as_view()),

    path('api/service/process', ProcessDevelopmentListAPI.as_view()),
    path('api/service/process/<int:pk>', ProcessDevelopmentDetailAPI.as_view()),
    path('api/service/<int:pk>/photo_present_project/delete', service_photo_present_project_delete),

    path('api/task', TaskListAPI.as_view()),
    path('api/task/add', TaskCreateAPI.as_view()),
    path('api/task/<int:pk>', TaskUpdateAPI.as_view()),
    path('api/task/<int:pk>/delete', TaskDestroyAPI.as_view()),
    path('api/task/<int:pk>/review', TaskReviewAPI.as_view()),

    path('api/project', ProjectListAPI.as_view()),
    path('api/project/<int:pk>', ProjectDetailAPI.as_view()),

    path('api/project/<int:pk>/cover/delete', project_cover_delete),
    path('api/project/<int:pk>/background_1/delete', project_b1_delete),
    path('api/project/<int:pk>/background_2/delete', project_b2_delete),
    # path('api/project/<int:pk>/add_service', project_add_service),
    # path('api/project/<int:pk>/delete_service', project_delete_service),

    path('api/project/small_photo', SmallPhotoProjectListAPI.as_view()),
    path('api/project/small_photo/<int:pk>', SmallPhotoProjectDetailAPI.as_view()),

    path('api/project/big_photo', BigPhotoProjectListAPI.as_view()),
    path('api/project/big_photo/<int:pk>', BigPhotoProjectDetailAPI.as_view()),

    path('api/project/block', ProjectBlockListAPI.as_view()),
    path('api/project/block/<int:pk>', ProjectBlockDetailAPI.as_view()),

    path('api/project/block/photo', ProjectBlockPhotoListAPI.as_view()),
    path('api/project/block/photo/<int:pk>', ProjectBlockPhotoDetailAPI.as_view()),

    path('api/review', ReviewListAPI.as_view()),
    path('api/review/<int:pk>', ReviewDetailAPI.as_view()),

    # re_path(r'^$', base_view),
    # # match all other pages
    # re_path(r'^.*$', base_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
