
# Register your models here.
from django.contrib import admin
from django.contrib.sessions.models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date', 'get_decoded')