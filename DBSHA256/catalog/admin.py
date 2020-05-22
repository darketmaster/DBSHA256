from django.contrib import admin
from .models import Release, SHA256OP


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'port', 'database', 'user', 'paramsFilter', 'created', 'generated')
    ordering = ('name',)
    search_fields = ('name', 'database')
    fieldsets = (
        (None, {
            'fields': ('name', ('ip', 'database'), ('user', 'password'))
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('port', 'paramsFilter'),
        }),
    )

class SHA256OPAdmin(admin.ModelAdmin):
    list_display = ('release', 'ptype', 'name', 'sha256', 'created')
    list_filter = ('release', 'ptype', 'created')
    ordering = ('release', 'ptype', 'name')
    search_fields = ('release', 'ptype', 'name')

admin.site.register(Release, ReleaseAdmin)
admin.site.register(SHA256OP, SHA256OPAdmin)