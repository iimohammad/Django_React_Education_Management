from django.contrib import admin
from .models import *


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number', 'mobile_number', 'address']


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'contactInfo', 'website_url', 'social_media_links']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'university', 'content', 'author', 'is_active', 'created_at']

