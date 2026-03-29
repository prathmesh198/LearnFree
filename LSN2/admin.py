from django.contrib import admin
from .models import user, course 


try:
    admin.site.register(user)
except admin.sites.AlreadyRegistered:
    pass


admin.site.register(course)