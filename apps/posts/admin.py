from django.contrib import admin

from .models import Like, Post


class LikeInline(admin.StackedInline):
    model = Like
    extra = 0


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]

    inlines = [LikeInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
