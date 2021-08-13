from django.contrib import admin

"""import models from models"""
from profiles_api import models

"""Register models which we have created"""
admin.site.register(models.UserProfile)
