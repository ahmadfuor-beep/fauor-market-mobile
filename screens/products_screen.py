import os

from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
    MDTopAppBarLeadingButtonContainer,
    MDTopAppBarTrailingButtonContainer,
    MDActionTopAppBarButton,
)

from services.data_service import load_products
from ui.theme import APP_COLORS


class ProductCard(MDCard):
    def __init__(self, product, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.add_callback = add_callback

        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(122)
        self.padding = dp(12)
        self.spacing = dp(12)
        self.radius = [22, 22, 22, 22]
        self.style = "filled"
        self.md_bg_color = APP_COLORS["surface"]
        self.line_color = APP_COLORS["border"]
        self.ripple_behavior = False

        image_path = os.path.join("assets", "images", product["image"])
        product_image = Image(
            source=image_path,
            size_hint=(0.26, 1),
            allow_stretch=True,
            keep_ratio=True,
        )

        info_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(0.50, 1),
            spacing=dp(4),
        )

        name_label = MDLabel(
            text=product["name"],
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Title",
            role="medium",
            bold=True,
        )

        price_label = MDLabel(
            text=f"{product['price']} NIS",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large",
        )

        category_label = MDLabel(
            text=product["category"],
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_style="Label",
            role="large",
        )

        info_box.add_widget(name_label)
        info_box.add_widget(price_label)
        info_box.add_widget(category_label)

        button_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(0.24, 1),
            adaptive_height=False,
        )

        spacer_top = MDBoxLayout()
        spacer_mid = MDBoxLayout(size_hint=(1, None), height=dp(8))
        spacer_bottom = MDBoxLayout()

        add_button = MDButton(
            MDButtonText(text="Add"),
            style="filled",
            size_hint=(1, None),
            height=dp(40),
            radius=[18, 18, 18, 18],
            md_bg_color=APP_COLORS["accent"],
            on_release=lambda x: self.add_callback(self.product),
        )

        button_box.add_widget(spacer_top)
        button_box.add_widget(add_button)
        button_box.add_widget(spacer_mid)
        button_box.add_widget(spacer_bottom)

        self.add_widget(product_image)
        self.add_widget(info_box)
        self.add_widget(button_box)


class ProductsScreen(MDScreen):
    def __init__(self, cart, **kwargs):
        super().__init__(**kwargs)
        self.cart = cart
        self.current_category = "All"
        self.search_text = ""

        self.md_bg_color = APP_COLORS["background"]

        self.root_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
        )

        self.add_widget(self.root_box)
        self.build_ui()

    def build_ui(self):
        self.root_box.clear_widgets()

        top_bar = MDTopAppBar(
            type="small",
            md_bg_color=APP_COLORS["surface_2"],
        )
        top_bar.add_widget(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="arrow-left",
                    on_release=self.go_back
                )
            )
        )
        top_bar.add_widget(
            MDTopAppBarTitle(
                text="Products",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"],
            )
        )
        top_bar.add_widget(
            MDTopAppBarTrailingButtonContainer(
                MDActionTopAppBarButton(icon="cart-outline")
            )
        )
        self.root_box.add_widget(top_bar)

        content_box = MDBoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(8), dp(14), dp(12)],
            spacing=dp(10),
        )

        self.search_field = MDTextField(
            hint_text="Search product...",
            text=self.search_text,
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )
        self.search_field.bind(text=self.on_search_text)
        content_box.add_widget(self.search_field)

        categories_box = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=dp(8),
        )

        for category in ["All", "Dairy", "Bakery", "Grains", "Oils"]:
            is_selected = category == self.current_category

            btn = MDButton(
                MDButtonText(text=category),
                style="filled" if is_selected else "outlined",
                size_hint=(None, None),
                height=dp(38),
                width=dp(92),
                radius=[18, 18, 18, 18],
                md_bg_color=APP_COLORS["accent_soft"] if is_selected else APP_COLORS["surface"],
                line_color=APP_COLORS["border"],
                on_release=lambda x, c=category: self.change_category(c),
            )
            categories_box.add_widget(btn)

        content_box.add_widget(categories_box)

        scroll = ScrollView(size_hint=(1, 1))

        products_list = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[0, dp(6), 0, dp(6)],
            size_hint_y=None,
        )
        products_list.bind(minimum_height=products_list.setter("height"))

        filtered_products = self.get_filtered_products()

        for product in filtered_products:
            products_list.add_widget(
                ProductCard(
                    product=product,
                    add_callback=self.add_to_cart
                )
            )

        if not filtered_products:
            products_list.add_widget(
                MDLabel(
                    text="No products found",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["muted"],
                    size_hint=(1, None),
                    height=dp(60),
                )
            )

        scroll.add_widget(products_list)
        content_box.add_widget(scroll)

        self.root_box.add_widget(content_box)

    def get_filtered_products(self):
        products = load_products()
        result = []

        for product in products:
            if self.current_category != "All" and product["category"] != self.current_category:
                continue

            if self.search_text.strip():
                if self.search_text.lower() not in product["name"].lower():
                    continue

            result.append(product)

        return result

    def change_category(self, category):
        self.current_category = category
        self.build_ui()

    def on_search_text(self, instance, value):
        self.search_text = value
        self.build_ui()

    def add_to_cart(self, product):
        self.cart.append(product)
        print(f"Added to cart: {product['name']}")
        print(self.cart)

    def go_back(self, *args):
        self.manager.current = "home"