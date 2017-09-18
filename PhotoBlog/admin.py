from django.contrib import admin

from .models import Project, Photo, Element

class PhotoInline(admin.TabularInline):
    model = Photo

class ElementInline(admin.TabularInline):
    model = Element
    ordering = ('order',)

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ElementInline, PhotoInline]
    
admin.site.register(Project, ProjectAdmin)