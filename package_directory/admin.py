from django.contrib import admin

from .models import Application, ApplicationAdmin

admin.site.register(Application, ApplicationAdmin)
