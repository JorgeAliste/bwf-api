from django.contrib import admin
from .models import Group, Event, UserProfile


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ('name', 'location', 'description')
    list_display = ('id', 'name', 'location', 'description')


@admin.register(UserProfile)
class GroupAdmin(admin.ModelAdmin):
    fields = ('user', 'image', 'is_premium', 'bio')
    list_display = ('id', 'user', 'image', 'is_premium', 'bio')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('team_1', 'team_2', 'time', 'score_1', 'score_2', 'group')
    list_display = ('id', 'team_1', 'team_2', 'time', 'score_1', 'score_2', 'group')
