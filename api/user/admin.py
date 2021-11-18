from django.contrib import admin

from .models import Education, Employment, EndUser, Follow, Location

# Register your models here.
admin.site.register(EndUser)
admin.site.register(Location)
admin.site.register(Education)
admin.site.register(Employment)
admin.site.register(Follow)
