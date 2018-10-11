from django.contrib import admin
from .models import (
    Post,
    Tag,
    Subscriber,
)


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'updated', 'read_time']
    readonly_fields = ['slug', 'read_time']
    list_display_links = ['updated']
    list_editable = ['title']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    save_on_top = True

    class Meta:
        model = Post


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    readonly_fields = ['slug']
    # list_display_links = ['title']
    # list_editable = ['title']
    # list_filter = ['title']
    # search_fields = ['title']

    class Meta:
        model = Tag


@admin.register(Subscriber)
class SubscriberModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email_address']

    class Meta:
        model = Subscriber
