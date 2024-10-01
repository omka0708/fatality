import json

from django.core.validators import RegexValidator
from django.db import models
from custom_admin.apps import photo_directory_path, cover_directory_path, user_directory_path, review_directory_path, \
    small_photo_project_directory_path, big_photo_project_directory_path, back1_project_directory_path, \
    back2_project_directory_path, cover_project_directory_path, present_project_directory_path, \
    site_user_directory_path, SERVER_HOSTNAME, block_project_directory_path
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    position = models.TextField(max_length=65535, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        ordering = ['id', ]


class SiteUser(models.Model):
    first_name = models.CharField(max_length=65535)
    last_name = models.CharField(max_length=65535)
    position = models.TextField(max_length=65535)
    avatar = models.ImageField(upload_to=site_user_directory_path, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id', ]


class Post(models.Model):
    title = models.CharField(max_length=65535)
    content = models.CharField(max_length=65535)

    title_sec1 = models.CharField(max_length=65535)
    content_sec1 = models.CharField(max_length=65535)

    middle_sec_text = models.CharField(max_length=65535, default='')

    title_sec2 = models.CharField(max_length=65535)
    content_sec2 = models.CharField(max_length=65535)

    cover = models.ImageField(upload_to=photo_directory_path)
    photo = models.ImageField(upload_to=cover_directory_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    introduction = models.CharField(max_length=65535, default='')

    class Meta:
        ordering = ['id', ]


class Service(models.Model):
    title = models.CharField(max_length=65535, unique=True)
    description = models.CharField(max_length=65535, default='')

    goals_objectives_text = models.CharField(max_length=65535, default='')

    title_sec1 = models.CharField(max_length=65535, default='')
    content_sec1 = models.CharField(max_length=65535, default='')
    title_sec2 = models.CharField(max_length=65535, default='')
    content_sec2 = models.CharField(max_length=65535, default='')

    title_process = models.CharField(max_length=65535, default='')
    mini_text = models.CharField(max_length=65535, default='', null=True, blank=True)
    title_present_project = models.CharField(max_length=65535, default='', null=True, blank=True)
    photo_present_project = models.ImageField(upload_to=present_project_directory_path, null=True, blank=True)

    class Meta:
        ordering = ['id', ]


class ProcessDevelopment(models.Model):
    title = models.CharField(max_length=65535)
    content = models.CharField(max_length=65535, default='')
    index_number = models.IntegerField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='processes', blank=True, null=True)

    class Meta:
        ordering = ['index_number', 'id']

    def __str__(self):
        return json.dumps({'id': self.id,
                           'index_number': self.index_number,
                           'title': self.title,
                           'content': self.content})


class Task(models.Model):
    name = models.CharField(max_length=65535)
    phone_number = models.CharField(max_length=65535)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='tasks')
    reviewed = models.BooleanField(default=False)
    comment = models.CharField(max_length=65535, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return json.dumps({'id': self.pk,
                           'name': self.name,
                           'phone_number': self.phone_number,
                           'reviewed': self.reviewed,
                           'comment': self.comment})

    class Meta:
        ordering = ['-id', ]


class Project(models.Model):
    title = models.CharField(max_length=65535)
    description = models.CharField(max_length=65535)
    about = models.CharField(max_length=65535)
    about_content = models.CharField(max_length=65535, default='')
    solution = models.CharField(max_length=65535)
    # service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='projects')
    # service = models.ManyToManyField(Service, related_name='projects')
    color = models.CharField(max_length=7,
                             validators=[RegexValidator(
                                 regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                                 message='Введите код цвета.'), ],
                             default='#ABCDEF')
    cover = models.ImageField(upload_to=cover_project_directory_path, null=True, blank=True)
    background_1 = models.ImageField(upload_to=back1_project_directory_path, null=True, blank=True)
    background_2 = models.ImageField(upload_to=back2_project_directory_path, null=True, blank=True)
    index_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return json.dumps({'id': self.pk,
                           'title': self.title})

    class Meta:
        ordering = ['id', ]


class ProjectBlock(models.Model):
    title = models.CharField(max_length=65535, blank=True)
    description = models.CharField(max_length=65535, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ProjectBlockPhoto(models.Model):
    title = models.CharField(max_length=65535, blank=True, default='')
    upload = models.ImageField(upload_to=block_project_directory_path)
    block = models.ForeignKey(ProjectBlock, on_delete=models.CASCADE, related_name='block_photos')
    index_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return json.dumps({'id': self.pk,
                           'title': self.title,
                           'upload': f'https://{SERVER_HOSTNAME}{self.upload.url}',
                           'index_number': self.index_number})


class SmallPhotoProject(models.Model):
    title = models.CharField(max_length=65535, default='')
    upload = models.ImageField(upload_to=small_photo_project_directory_path)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='small_photos')
    index_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return json.dumps({'id': self.pk,
                           'title': self.title,
                           'upload': f'https://{SERVER_HOSTNAME}{self.upload.url}',
                           'index_number': self.index_number})

    class Meta:
        ordering = ['id', ]


class BigPhotoProject(models.Model):
    title = models.CharField(max_length=65535, default='')
    upload = models.ImageField(upload_to=big_photo_project_directory_path)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='big_photos')
    index_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return json.dumps({'id': self.pk,
                           'upload': f'https://{SERVER_HOSTNAME}{self.upload.url}',
                           'index_number': self.index_number})

    class Meta:
        ordering = ['id', ]


class Review(models.Model):
    title = models.CharField(max_length=65535)
    description = models.CharField(max_length=65535, default='')
    photo = models.ImageField(upload_to=review_directory_path, null=True, blank=True)

    class Meta:
        ordering = ['id', ]
