from django.contrib import admin

from reaction.models import React, Reaction, UserReaction, ReactionSettings


class ReactAdmin(admin.ModelAdmin):
    list_display = ('slug', 'emoji', 'source_file')
    search_fields = ('slug', 'emoji')


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('content_obj', 'urlhash', 'settings')
    readonly_fields = ('content_type', 'urlhash', 'object_id', 'content_object', 'settings')

    def content_obj(self, obj):
        return f'{obj.content_type} - {obj.content_object}'

    content_obj.short_description = 'Content Object'


class UserReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'react', 'reaction')
    readonly_fields = ('user', 'react', 'reaction')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'react_type')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(React, ReactAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(UserReaction, UserReactionAdmin)
admin.site.register(ReactionSettings, SettingsAdmin)
