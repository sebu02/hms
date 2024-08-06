from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Departments)
admin.site.register(Patient_Records)

