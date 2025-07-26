from django.core.management.base import BaseCommand
from menu.models import MenuItem


class Command(BaseCommand):
    help = "Creates test menu structure"

    def handle(self, *args, **options):
        MenuItem.objects.all().delete()

        root = MenuItem.objects.create(
            name="Root", menu_name="main_menu", url="/",
            order=0
        )

        about = MenuItem.objects.create(
            name="About", menu_name="main_menu", url="/about/", parent=root,
            order=0
        )

        purpose = MenuItem.objects.create(
            name="Purpose",
            menu_name="main_menu",
            url="/about/purpose/",
            parent=about,
            order=0
        )

        products = MenuItem.objects.create(
            name="Products",
            menu_name="main_menu",
            url="/about/products/",
            parent=about,
            order=1
        )

        product1 = MenuItem.objects.create(
            name="Product 1",
            menu_name="main_menu",
            url="/about/products/product1/",
            parent=products,
            order=0
        )

        detail1 = MenuItem.objects.create(
            name="Detail 1",
            menu_name="main_menu",
            url="/about/products/product1/detail1/",
            parent=product1,
        )

        product2 = MenuItem.objects.create(
            name="Product 2",
            menu_name="main_menu",
            url="/about/products/product2/",
            parent=products,
            order=1
        )

        team = MenuItem.objects.create(
            name="Team", menu_name="main_menu", url="/about/team/", parent=about,
            order=2
        )

        contacts = MenuItem.objects.create(
            name="Contacts",
            menu_name="main_menu",
            url="/contacts/",
            parent=root,
            order=1
        )

        address = MenuItem.objects.create(
            name="Address", menu_name="footer_menu", url="/address/",
            order=0
        )

        help_item = MenuItem.objects.create(
            name="Help", menu_name="footer_menu", url="/help/",
            order=1
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully created test menu structure")
        )
