from django.contrib import admin
from .models import Post, Contact

# Register your models here.
# @admin.register(Post)
# class PostModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'desc', 'title_tag', 'post_date', 'post_image']


admin.site.register(Post)
admin.site.register(Contact)
