import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from app_shop.models import (
    Product,
    ProductColor,
    SpecialOffer,
)

fake = Faker()

COLORS = [
    ("Black", "#000000"),
    ("White", "#FFFFFF"),
    ("Red", "#FF0000"),
    ("Blue", "#0000FF"),
    ("Green", "#00FF00"),
    ("Yellow", "#FFFF00"),
    ("Gray", "#808080"),
    ("Pink", "#FFC0CB"),
    ("Purple", "#800080"),
    ("Orange", "#FFA500"),
]


class Command(BaseCommand):
    help = "Seed database with fake data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of products to create"
        )

    def handle(self, *args, **options):
        count = options["count"]

        self.stdout.write("Deleting old data...")

        ProductColor.objects.all().delete()
        Product.objects.all().delete()
        SpecialOffer.objects.all().delete()

        self.stdout.write("Creating Products...")

        for _ in range(count):
            product = Product.objects.create(
                title=fake.unique.word().title(),
                sub_title=fake.sentence(nb_words=4),
            )

            selected_colors = random.sample(
                COLORS,
                random.randint(1, 4)
            )

            for color_name, color_code in selected_colors:
                price = random.randint(100, 5000)

                ProductColor.objects.create(
                    product=product,
                    name=color_name,
                    color_code=color_code,
                    price=price,
                    price_with_discount=price - random.randint(10, int(price * 0.3)),
                )

        self.stdout.write("Creating Special Offers...")

        for _ in range(40):
            SpecialOffer.objects.create(
                image="offers/sample.jpg",  # مسیر یک عکس تست
                link=fake.url(),
                location=fake.city(),
                datetime=fake.future_datetime(),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"""
Done!

Products: {Product.objects.count()}
Product Colors: {ProductColor.objects.count()}
Special Offers: {SpecialOffer.objects.count()}
"""
            )
        )
