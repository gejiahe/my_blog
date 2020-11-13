from django.contrib import admin
from .models import ArticlePost,ArticleColumn
# Register your models here.


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ['author','title','body','total_views']


admin.site.register(ArticlePost,ArticlePostAdmin)
admin.site.register(ArticleColumn)
