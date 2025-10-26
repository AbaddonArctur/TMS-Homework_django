from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/add/", views.add_recipe, name="add_recipe"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/<int:pk>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:pk>/delete/", views.delete_recipe, name="delete_recipe"),
    path("recipe/<int:pk>/comment/", views.recipe_comment_post, name="recipe_comment_post"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("register/", views.register_view, name="register"),
    path("register/submit/", views.register_post, name="register_post"),
    path("login/", views.login_view, name="login"),
    path("login/submit/", views.login_post, name="login_post"),
    path("logout/", views.logout_view, name="logout"),
]