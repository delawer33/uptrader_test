from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.test import RequestFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext

from .models import MenuItem
from .templatetags.menu_tags import draw_menu


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.root = MenuItem.objects.create(
            name="Главная", menu_name="main_menu", url="/"
        )
        self.about = MenuItem.objects.create(
            name="О нас", menu_name="main_menu", parent=self.root, url="/about/"
        )
        self.contacts = MenuItem.objects.create(
            name="Контакты",
            menu_name="main_menu",
            parent=self.root,
            named_url="contacts",
        )

    def test_get_url(self):
        self.assertEqual(self.root.get_url(), "/")
        self.assertEqual(self.about.get_url(), "/about/")
        self.assertEqual(self.contacts.get_url(), "/contacts/")

    def test_str_representation(self):
        self.assertEqual(str(self.root), "Главная")

    def test_parent_relationship(self):
        self.assertEqual(self.about.parent, self.root)
        self.assertEqual(self.contacts.parent, self.root)

        children = list(self.root.children.all())
        self.assertEqual(children, [self.about, self.contacts])

    def test_ordering(self):
        item1 = MenuItem.objects.create(
            name="Первый", menu_name="test", order=2
        )
        item2 = MenuItem.objects.create(
            name="Второй", menu_name="test", order=1
        )

        items = MenuItem.objects.filter(menu_name="test")
        self.assertEqual(list(items), [item2, item1])

    def test_validation(self):
        invalid_item = MenuItem(name="Invalid", menu_name="main_menu")
        with self.assertRaises(ValidationError):
            invalid_item.full_clean()


class MenuTagTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Структура
        #  root
        #     ├── about
        #     │    ├── purpose
        #     │    ├── products
        #     │    │     ├── product1
        #                    └── detail1
        #     │    │     └── product2
        #     │    └── team
        #     └── contacts (активный)

        self.root = MenuItem.objects.create(
            name="Root", menu_name="main_menu", url="/", order=1
        )

        self.about = MenuItem.objects.create(
            name="About",
            menu_name="main_menu",
            parent=self.root,
            url="/about/",
            order=1,
        )
        self.contacts = MenuItem.objects.create(
            name="Contacts",
            menu_name="main_menu",
            parent=self.root,
            url="/contacts/",
            order=2,
        )

        self.purpose = MenuItem.objects.create(
            name="Purpose",
            menu_name="main_menu",
            parent=self.about,
            url="/purpose/",
            order=1,
        )
        self.products = MenuItem.objects.create(
            name="Products",
            menu_name="main_menu",
            parent=self.about,
            url="/products/",
            order=2,
        )
        self.team = MenuItem.objects.create(
            name="Team",
            menu_name="main_menu",
            parent=self.about,
            url="/team/",
            order=3,
        )

        self.product1 = MenuItem.objects.create(
            name="Product 1",
            menu_name="main_menu",
            parent=self.products,
            url="/product1/",
            order=1,
        )
        self.product2 = MenuItem.objects.create(
            name="Product 2",
            menu_name="main_menu",
            parent=self.products,
            url="/product2/",
            order=2,
        )

        self.detail1 = MenuItem.objects.create(
            name="Detail 1",
            menu_name="main_menu",
            parent=self.product1,
            url="/detail1/",
            order=1,
        )

    def test_active_contacts_expansion(self):
        request = self.factory.get("/contacts/")
        context = {"request": request}

        result = draw_menu(context, "main_menu")

        # Проверяем что contact активный
        self.assertEqual(result["active_item"], self.contacts)

        # Contact должен быть развернут
        self.assertIn(self.root.id, result["expanded_ids"])

        # Все пункты, которые должны быть развернуты
        # """Все, что над выделенным пунктом - развернуто"""
        all_items = [
            self.root,
            self.about,
            self.contacts,
            self.purpose,
            self.products,
            self.team,
            self.product1,
            self.product2,
            self.detail1,
        ]

        for item in all_items:
            self.assertIn(
                item.id,
                result["expanded_ids"],
                f"{item.name} должен быть в expanded_ids",
            )

        # Провека структур объектов в результате

        root = result["root_items"][0]
        self.assertEqual(root.name, "Root")
        self.assertEqual(len(root.children_list), 2)

        about = next(c for c in root.children_list if c.name == "About")
        self.assertEqual(len(about.children_list), 3)
        self.assertTrue(
            all(
                c.name in ["Purpose", "Products", "Team"]
                for c in about.children_list
            )
        )

        products = next(c for c in about.children_list if c.name == "Products")
        self.assertEqual(len(products.children_list), 2)
        self.assertTrue(
            all(
                c.name in ["Product 1", "Product 2"]
                for c in products.children_list
            )
        )

    def test_active_product1_expansion(self):
        request = self.factory.get("/product1/")
        context = {"request": request}

        result = draw_menu(context, "main_menu")

        self.assertEqual(result["active_item"], self.product1)

        # Все пункты над Product 1
        items_above = [
            self.root,
            self.about,
            self.products,
            self.purpose,
            self.team,
            self.product1,
            self.detail1,
        ]

        for item in items_above:
            self.assertIn(item.id, result["expanded_ids"])

    def test_active_root_expansion(self):
        request = self.factory.get("/")
        context = {"request": request}

        result = draw_menu(context, "main_menu")

        # Проверяем что root активный
        self.assertEqual(result["active_item"], self.root)

        # Root должен быть развернут
        self.assertIn(self.root.id, result["expanded_ids"])

        # Первый уровень под Root должен быть развернут
        for item in [self.about, self.contacts]:
            self.assertIn(
                item.id,
                result["expanded_ids"],
                f"{item.name} должен быть развернут",
            )

        # Второй уровень не должен быть развернут
        for item in [self.purpose, self.products, self.team]:
            self.assertNotIn(
                item.id,
                result["expanded_ids"],
                f"{item.name} не должен быть развернут",
            )

    def test_only_one_query(self):
        request = self.factory.get("/contacts/")
        context = {"request": request}

        with CaptureQueriesContext(connection) as queries:
            draw_menu(context, "main_menu")
            self.assertEqual(len(queries), 1)

