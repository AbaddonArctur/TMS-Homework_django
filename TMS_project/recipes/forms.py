from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Recipe, Comment, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "category", "description", "instructions", "image"]
        labels = {
            "title": "Название рецепта",
            "category": "Категория",
            "description": "Описание",
            "instructions": "Пошаговая инструкция",
            "image": "Изображение",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "rows": 4,
                    "style": "resize: none; overflow-y: hidden;"
                })


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "amount"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Мука"}
            ),
            "amount": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "200 г"}
            ),
        }


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Комментарий"}
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Напишите комментарий...",
                    "style": "resize: none; overflow-y: hidden;"
                }
            )
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    verify_password = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"] = self.fields.pop("password")
        self.fields["password2"] = self.fields.pop("verify_password")
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})