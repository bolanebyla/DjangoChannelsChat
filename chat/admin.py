from django.contrib import admin
from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creation_date', 'update_date')
    search_fields = ('title',)
    ordering = ['-update_date']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'chat', 'sender', 'creation_date', 'update_date')
    search_fields = ('text',)
    ordering = ['-creation_date']
