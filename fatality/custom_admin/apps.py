# import requests
import shortuuid
from django.apps import AppConfig
from drf_spectacular.extensions import OpenApiAuthenticationExtension

SERVICE_DESCRIPTION = ('service_id: '
                       '1 - "Разработка приложений"; '
                       '2 - "Разработка сайтов"; '
                       '3 - "Разработка CRM"; '
                       '4 - "Разработка агрегаторов доставки"; '
                       '5 - "Разработка дизайна"; '
                       '6 - "Реклама и CEO".')

# SERVER_HOSTNAME = requests.get("https://httpbin.org/ip").json()['origin']
SERVER_HOSTNAME = 'fatalitystudio.ru'


def photo_directory_path(instance, filename):
    return f"blog/photos/{str(shortuuid.uuid())}/{filename}"


def cover_directory_path(instance, filename):
    return f"blog/covers/{str(shortuuid.uuid())}/{filename}"


def user_directory_path(instance, filename):
    return f"user/{str(shortuuid.uuid())}/{filename}"


def site_user_directory_path(instance, filename):
    return f"site_user/{str(shortuuid.uuid())}/{filename}"


def review_directory_path(instance, filename):
    return f"review/{str(shortuuid.uuid())}/{filename}"


def small_photo_project_directory_path(instance, filename):
    return f"project/small/{str(shortuuid.uuid())}/{filename}"


def big_photo_project_directory_path(instance, filename):
    return f"project/big/{str(shortuuid.uuid())}/{filename}"


def cover_project_directory_path(instance, filename):
    return f"project/cover/{str(shortuuid.uuid())}/{filename}"


def back1_project_directory_path(instance, filename):
    return f"project/background_1/{str(shortuuid.uuid())}/{filename}"


def back2_project_directory_path(instance, filename):
    return f"project/background_2/{str(shortuuid.uuid())}/{filename}"


def block_project_directory_path(instance, filename):
    return f"project/block/photo/{str(shortuuid.uuid())}/{filename}"


def present_project_directory_path(instance, filename):
    return f"service/present/{str(shortuuid.uuid())}/{filename}"


class CustomAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_admin'


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'knox.auth.TokenAuthentication'
    name = 'knoxTokenAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Авторизация на основе токена. Формат: Token <действующий токен>'
        }
