from django.contrib import admin
from core import models

# Register your models here.

admin.site.register(models.Item)
admin.site.register(models.Sort)
admin.site.register(models.Accepted)

admin.site.register(models.Payment)
admin.site.register(models.News)
admin.site.register(models.Job)
admin.site.register(models.Messages)
admin.site.register(models.Video)
admin.site.register(models.Slider)