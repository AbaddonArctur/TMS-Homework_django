from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("add/", views.add_recipe, name="add_recipe"),
    path("edit/<int:pk>/", views.edit_recipe, name="edit_recipe"),
    path("delete/<int:pk>/", views.delete_recipe, name="delete_recipe"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]