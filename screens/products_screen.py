from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import os

from services.data_service import load_products

################################################
class ProductsScreen(Screen):
    def __init__(self, cart, **kwargs):
        super().__init__(**kwargs)
        self.cart = cart

        self.main_layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.add_widget(self.main_layout)
        self.load_products_ui("All")

    def load_products_ui(self, category="All"):
        self.main_layout.clear_widgets()

        title_label = Label(
            text="Products",
            font_size=30,
            size_hint=(1, None),
            height=dp(50)
        )
        self.main_layout.add_widget(title_label)

        categories_layout = BoxLayout(
            size_hint=(1, None),
            height=dp(50),
            spacing=5
        )

        categories = ["All", "Dairy", "Bakery", "Grains", "Oils"]

        for cat in categories:
            btn = Button(
                text=cat,
                background_normal="",
                background_color=(0.2, 0.6, 0.2, 1)
            )
            btn.bind(on_press=lambda instance, c=cat: self.load_products_ui(c))
            categories_layout.add_widget(btn)

        self.main_layout.add_widget(categories_layout)

        scroll_view = ScrollView(size_hint=(1, 1))

        products_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        products_layout.bind(minimum_height=products_layout.setter("height"))

        products = load_products()

        for product in products:
            if category != "All" and product["category"] != category:
                continue

            product_box = BoxLayout(
                size_hint=(1, None),
                height=dp(120),
                spacing=10,
                padding=10
            )

            image_path = os.path.join("assets", "images", product["image"])

            product_image = Image(
                source=image_path,
                size_hint=(0.25, 1)
            )

            product_info = BoxLayout(
                orientation="vertical",
                size_hint=(0.5, 1),
                spacing=5
            )

            name_label = Label(
                text=product["name"],
                font_size=20
            )

            price_label = Label(
                text=f"{product['price']} NIS",
                font_size=16
            )

            category_label = Label(
                text=product["category"],
                font_size=14
            )

            product_info.add_widget(name_label)
            product_info.add_widget(price_label)
            product_info.add_widget(category_label)

            add_button = Button(
                text="Add",
                size_hint=(0.25, 1),
                background_normal="",
                background_color=(0.1, 0.5, 0.8, 1)
            )

            add_button.bind(
                on_press=lambda instance, p=product: self.add_to_cart(p)
            )

            product_box.add_widget(product_image)
            product_box.add_widget(product_info)
            product_box.add_widget(add_button)

            products_layout.add_widget(product_box)
        # add products layout to scroll view and then to main layout
        scroll_view.add_widget(products_layout)
        self.main_layout.add_widget(scroll_view)

        back_button = Button(
            text="Back to Home",
            size_hint=(1, None),
            height=dp(50),
            background_normal="",
            background_color=(0.8, 0.2, 0.2, 1)
        )

        back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_button)

    def add_to_cart(self, product):
        self.cart.append(product)
        print(f"Added to cart: {product['name']}")
        print(self.cart)

    def go_back(self, instance):
        self.manager.current = "home"