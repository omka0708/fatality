from django.contrib import admin
from .models import User, Post, Task, Service, Project

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Task)
admin.site.register(Service)
admin.site.register(Project)
