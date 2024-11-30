from django.contrib import admin
from .models import Post, Category, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title", "slug", "is_published", "created_at"
    )
    search_fields = ("title", "slug")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
    fieldsets = (
        (None, {
            "fields": ("title", "description", "slug", "is_published"),
            "description": "Настройка категории",
        }),
        ("Дополнительно", {
            "fields": ("created_at",),
        }),
    )
    readonly_fields = ("created_at",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name", "is_published", "created_at"
    )
    search_fields = ("name",)
    list_filter = ("is_published",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author", "category",
        "pub_date", "is_published", "created_at"
    )
    search_fields = ("title", "text")
    list_filter = ("is_published", "pub_date", "category")
    ordering = ("-pub_date",)
    fieldsets = (
        (None, {
            "fields": (
                "title", "text", "pub_date",
                "is_published", "author"
            ),
        }),
        ("Связи", {
            "fields": ("category", "location"),
        }),
        ("Дополнительно", {
            "fields": ("created_at",),
        }),
    )
    readonly_fields = ("created_at",)
