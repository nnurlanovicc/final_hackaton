from django.contrib import admin
from .models import ProfileRecruiter, ProfileUser

admin.site.register(ProfileUser)
admin.site.register(ProfileRecruiter)
