import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Comment


class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными (faker). Можно указать количество объектов и очистить старые."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="Количество создаваемых пользователей (по умолчанию: 5).",
        )
        parser.add_argument(
            "--recipes",
            type=int,
            default=10,
            help="Количество создаваемых рецептов (по умолчанию: 10).",
        )
        parser.add_argument(
            "--ingredients",
            type=int,
            default=3,
            help="Среднее количество ингредиентов на рецепт (по умолчанию: 3).",
        )
        parser.add_argument(
            "--comments",
            type=int,
            default=4,
            help="Среднее количество комментариев на рецепт (по умолчанию: 4).",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистить все данные перед созданием новых.",
        )

    def handle(self, *args, **options):
        fake = Faker("ru_RU")

        num_users = options["users"]
        num_recipes = options["recipes"]
        avg_ingredients = options["ingredients"]
        avg_comments = options["comments"]
        clear_data = options["clear"]

        if clear_data:
            Comment.objects.all().delete()
            Ingredient.objects.all().delete()
            Recipe.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            self.stdout.write(self.style.SUCCESS("Все старые данные удалены."))

        self.stdout.write(self.style.WARNING("Генерация тестовых данных..."))

        users = []
        for i in range(num_users):
            username = f"user{i + 1}"
            user, _ = User.objects.get_or_create(username=username)
            user.set_password("12345")
            user.save()
            users.append(user)
        self.stdout.write(f"Создано {len(users)} пользователей.")

        recipes = []
        for _ in range(num_recipes):
            author = random.choice(users)
            recipe = Recipe.objects.create(
                title=fake.sentence(nb_words=3),
                category=random.choice(["Супы", "Салаты", "Десерты", "Закуски", "Основные блюда"]),
                description=fake.text(max_nb_chars=200),
                instructions=fake.text(max_nb_chars=500),
                author=author,
            )
            recipes.append(recipe)

            for _ in range(random.randint(1, avg_ingredients + 2)):
                Ingredient.objects.create(
                    recipe=recipe,
                    name=fake.word(),
                    amount=f"{random.randint(1, 5)} {random.choice(['г', 'шт', 'ст.л.', 'ч.л.'])}",
                )

        self.stdout.write(f"Создано {len(recipes)} рецептов и ингредиенты к ним.")

        total_comments = 0
        for recipe in recipes:
            for _ in range(random.randint(1, avg_comments)):
                author = random.choice(users)
                comment = Comment.objects.create(
                    recipe=recipe,
                    author=author,
                    text=fake.sentence(nb_words=10),
                )
                total_comments += 1

                if random.choice([True, False]):
                    reply_author = random.choice(users)
                    Comment.objects.create(
                        recipe=recipe,
                        author=reply_author,
                        parent=comment,
                        text=fake.sentence(nb_words=8),
                    )
                    total_comments += 1

        self.stdout.write(f"Создано {total_comments} комментариев.")
        self.stdout.write(self.style.SUCCESS("База успешно заполнена тестовыми данными!"))
