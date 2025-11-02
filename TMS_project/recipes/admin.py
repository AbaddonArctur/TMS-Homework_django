from django.contrib import admin
from .models import Recipe, Ingredient, Comment


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = "recipe"
    extra = 0
    fields = ("author", "text", "parent", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at")
    list_filter = ("category", "author", "created_at")
    search_fields = ("title", "category", "author__username")
    inlines = [IngredientInline, CommentInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "recipe")
    search_fields = ("name", "recipe__title")


class ReplyInline(admin.TabularInline):
    model = Comment
    fk_name = "parent"
    extra = 0
    fields = ("author", "text", "created_at")
    readonly_fields = ("created_at",)
    verbose_name_plural = "Ответы на комментарий"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe", "parent", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("author__username", "text", "recipe__title")
    inlines = [ReplyInline]
