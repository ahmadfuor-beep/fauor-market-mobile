import os
from kivy.animation import Animation
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
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
from services.db_service import get_products, add_to_cart_db
from ui.theme import APP_COLORS

class ProductCard(MDCard):
    def __init__(self, product, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.add_callback = add_callback

        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = dp(300)
        self.padding = dp(12)
        self.spacing = dp(8)
        self.radius = [24, 24, 24, 24]
        self.style = "filled"
        self.md_bg_color = APP_COLORS["surface"]
        self.line_color = APP_COLORS["border"]
        self.ripple_behavior = False

        image_path = os.path.join("assets", "images", product["image"])

        image_box = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(110),
            padding=[dp(8), dp(8), dp(8), dp(0)]
        )

        left_space = MDBoxLayout()
        right_space = MDBoxLayout()

        product_image = Image(
            source=image_path,
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={"center_y": 0.5}
        )

        image_box.add_widget(left_space)
        image_box.add_widget(product_image)
        image_box.add_widget(right_space)

        name_label = MDLabel(
            text=product["name"],
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Title",
            role="medium",
            bold=True,
            size_hint=(1, None),
            height=dp(30)
        )

        price_label = MDLabel(
            text=f"{product['price']} NIS",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large",
            size_hint=(1, None),
            height=dp(28)
        )

        category_label = MDLabel(
            text=product["category"],
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_style="Label",
            role="large",
            size_hint=(1, None),
            height=dp(24)
        )

        button_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(50),
            padding=[0, dp(4), 0, 0]
        )

        left_space = MDBoxLayout()
        right_space = MDBoxLayout()

        add_button = MDButton(
            MDButtonText(text="Add"),
            style="filled",
            size_hint=(None, None),
            width=dp(82),
            height=dp(38),
            radius=[19, 19, 19, 19],
            md_bg_color=APP_COLORS["accent"],
            on_release=lambda x: self.animate_and_add()
        )

        button_row.add_widget(left_space)
        button_row.add_widget(add_button)
        button_row.add_widget(right_space)

        self.add_widget(image_box)
        self.add_widget(name_label)
        self.add_widget(price_label)
        self.add_widget(category_label)
        self.add_widget(button_row)
        # start with invisible card for animation effect
        self.opacity = 0

        Animation(opacity=1, duration=0.4).start(self)
        
    def animate_and_add(self):
        anim = Animation(opacity=0.5, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.start(self)

        self.add_callback(self.product)    
    

    

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

        products_list = GridLayout(
            cols=2,
            spacing=dp(12),
            padding=[0, dp(6), 0, dp(6)],
            size_hint_y=None
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
        products = get_products()
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
        add_to_cart_db(product)

        snackbar = MDSnackbar(
            MDSnackbarText(text=f"{product['name']} added to cart")
        )
        snackbar.open()

    def go_back(self, *args):
        self.manager.current = "home"