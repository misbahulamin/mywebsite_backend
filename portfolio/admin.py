from django.contrib import admin
from .models import MyProject

class MyProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technology_stack', 'live', 'code_link', 'my_role')
    search_fields = ('title', 'description', 'technology_stack')
    list_filter = ('technology_stack',)
    readonly_fields = ('id',)  # To make `id` field readonly (optional)

admin.site.register(MyProject, MyProjectAdmin)
