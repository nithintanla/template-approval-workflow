from django.contrib import admin
from .models import Brand, Template

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'message_type', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'message_type', 'brand')
    search_fields = ('title', 'content')
