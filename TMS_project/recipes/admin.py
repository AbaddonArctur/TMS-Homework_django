from django.contrib import admin
from .models import Recipe, Ingredient, Comment

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at")
    list_filter = ("category", "author", "created_at")
    search_fields = ("title", "category", "author__username")
    inlines = [IngredientInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("author__username", "text", "recipe__title")