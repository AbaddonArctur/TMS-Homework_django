from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Comment
from faker import Faker
import random

fake = Faker("ru_RU")

class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username="test_user")
        if created:
            user.set_password("password123")
            user.save()

        for _ in range(10):
            recipe = Recipe.objects.create(
                title=fake.sentence(nb_words=3),
                category=random.choice(["Салаты", "Десерты", "Основные блюда"]),
                description=fake.paragraph(nb_sentences=3),
                instructions=fake.text(max_nb_chars=200),
                author=user,
            )

            for _ in range(random.randint(2, 5)):
                Ingredient.objects.create(
                    recipe=recipe,
                    name=fake.word(),
                    amount=f"{random.randint(1, 300)} г"
                )

            for _ in range(random.randint(1, 3)):
                Comment.objects.create(
                    recipe=recipe,
                    author=user,
                    text=fake.sentence(),
                )

        self.stdout.write(self.style.SUCCESS("База данных заполнена тестовыми данными"))