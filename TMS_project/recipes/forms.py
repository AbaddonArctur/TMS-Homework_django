from django import forms
from .models import Recipe, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "category", "description", "ingredients", "instructions", "image"]
        labels = {
            "title": "Название рецепта",
            "category": "Категория",
            "description": "Краткое описание",
            "ingredients": "Ингредиенты",
            "instructions": "Пошаговая инструкция",
            "image": "Изображение",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "style": "max-width: 500px;"
            })

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Комментарий"}
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Напишите комментарий..."
            })
        }

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "style": "max-width: 400px;"
            })