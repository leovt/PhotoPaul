from django.conf.urls import url

from . import views

app_name = 'PhotoBlog'

urlpatterns = [
    url(r'^(?P<project_id>[0-9]+)/photos$', views.gallery, name='gallery'),
    url(r'^(?P<project_id>[0-9]+)/edit$', views.editor, name='editor'),
    url(r'^(?P<project_id>[0-9]+)/insert$', views.insert, name='insert'),
    url(r'^(?P<project_id>[0-9]+)/upload$', views.upload, name='upload'),
    url(r'^(?P<project_id>[0-9]+)/?$', views.blog, name='blog'),
    url(r'^create$', views.create, name='create'),
    url(r'^$', views.bloglist, name='list'),
    url(r'^elements/(?P<element_id>[0-9]+)$', views.element, name='element'),
    ]