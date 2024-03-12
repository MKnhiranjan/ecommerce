from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')

class LoggedInUserAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'last_activity')

    def get_username(self, obj):
        return obj.get_decoded().get('_auth_user_id')
    get_username.short_description = 'User ID'

    def last_activity(self, obj):
        try:
            session = Session.objects.get(session_key=obj.session_key)
            last_activity = session.last_activity
            now = timezone.now()
            if now - last_activity > timezone.timedelta(seconds=300):  # Adjust time threshold as needed
                return 'Inactive'
            return 'Active'
        except Session.DoesNotExist:
            return 'Unknown'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Session, LoggedInUserAdmin)
from .models import *
admin.site.register(Product)