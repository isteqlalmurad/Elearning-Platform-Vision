from django.contrib import admin

# Register your models here in order to be applied on the admin panel in the 
from .models import UserProfile
from .models import Progress
admin.site.register(UserProfile)
admin.site.register(Progress)