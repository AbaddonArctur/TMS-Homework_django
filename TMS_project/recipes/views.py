from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm, RegisterForm, IngredientFormSet

@require_GET
def index(request):
    q = request.GET.get("q", "")
    category = request.GET.get("category", "")
    recipes = Recipe.objects.all().order_by("-created_at")

    if q:
        recipes = recipes.filter(title__icontains=q) | recipes.filter(ingredients__icontains=q)
    if category:
        recipes = recipes.filter(category__icontains=category)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {"page_obj": page_obj, "q": q, "category": category})

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            formset.instance = recipe
            formset.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = IngredientFormSet()

    return render(request, "add_recipe.html", {"form": form, "formset": formset})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.filter(parent__isnull=True).order_by("-created_at")
    form = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get("parent_id")
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user

            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id, recipe=recipe).first()
                if parent_comment:
                    comment.parent = parent_comment

            comment.save()
            return redirect("recipe_detail", pk=recipe.id)

    return render(request, "recipe_detail.html", {
        "recipe": recipe,
        "comments": comments,
        "form": form,
    })

@login_required
@require_POST
def recipe_comment_post(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.author = request.user

        parent_id = request.POST.get("parent_id")

        if parent_id:
            parent_comment = Comment.objects.filter(id=parent_id, recipe=recipe).first()
            if parent_comment:
                comment.parent = parent_comment

        comment.save()

    return redirect("recipe_detail", pk=recipe.id)

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return redirect("index")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)

    return render(request, "edit_recipe.html", {
        "form": form,
        "formset": formset,
        "recipe": recipe,
    })

@login_required
@require_POST
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author == request.user:
        recipe.delete()
    return redirect("index")

@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    recipe = comment.recipe

    if comment.author == request.user:
        comment.delete()
    return redirect("recipe_detail", pk=recipe.id)

@require_GET
def register_view(request):
    form = RegisterForm()
    return render(request, "register.html", {"form": form})

@require_POST
def register_post(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "register.html", {"form": form})

@require_GET
def login_view(request):
    return render(request, "login.html")

@require_POST
def login_post(request):
    username_error = ""
    password_error = ""

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()

    if not username:
        username_error = "Обязательное поле."
    if not password:
        password_error = "Обязательное поле."

    if username and password:
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            password_error = "Неверное имя пользователя или пароль."

    return render(request, "login.html", {
        "username_error": username_error,
        "password_error": password_error,
    })

@login_required
@require_GET
def logout_view(request):
    logout(request)
    return redirect("index")