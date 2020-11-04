from django.urls import path
from . import views
# Django2.0之后，app的urls.py必须配置app_name，否则会报错。
app_name='article'


urlpatterns = [
    path('article_list/',views.article_list,name='article_list')
]
