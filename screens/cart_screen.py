from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
    MDTopAppBarLeadingButtonContainer,
    MDActionTopAppBarButton,
)

from ui.theme import APP_COLORS


class CartItemCard(MDCard):
    def __init__(self, product, remove_callback, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(92)
        self.padding = dp(14)
        self.spacing = dp(12)
        self.radius = [22, 22, 22, 22]
        self.style = "filled"
        self.md_bg_color = APP_COLORS["surface"]
        self.line_color = APP_COLORS["border"]

        info_box = MDBoxLayout(
            orientation="vertical"
        )

        name_label = MDLabel(
            text=product["name"],
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Title",
            role="medium",
            bold=True
        )

        price_label = MDLabel(
            text=f"{product['price']} NIS",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large"
        )

        info_box.add_widget(name_label)
        info_box.add_widget(price_label)

        remove_button = MDButton(
            MDButtonText(text="Remove"),
            style="outlined",
            size_hint=(None, None),
            width=dp(100),
            height=dp(40),
            radius=[18, 18, 18, 18],
            line_color=APP_COLORS["border"],
            on_release=lambda x: remove_callback(product)
        )

        self.add_widget(info_box)
        self.add_widget(remove_button)


class CartScreen(MDScreen):
    def __init__(self, cart, **kwargs):
        super().__init__(**kwargs)
        self.cart = cart

        self.md_bg_color = APP_COLORS["background"]

        self.root_box = MDBoxLayout(
            orientation="vertical"
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
                text="My Cart",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"]
            )
        )

        self.root_box.add_widget(top_bar)

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(12)
        )

        scroll = ScrollView(size_hint=(1, 1))

        self.items_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )
        self.items_box.bind(minimum_height=self.items_box.setter("height"))

        scroll.add_widget(self.items_box)
        content.add_widget(scroll)

        self.total_label = MDLabel(
            text="Total: 0 NIS",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Title",
            role="large",
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )
        content.add_widget(self.total_label)

        buttons_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(48),
            spacing=dp(10)
        )

        clear_button = MDButton(
            MDButtonText(text="Clear Cart"),
            style="outlined",
            size_hint=(0.5, 1),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.clear_cart
        )

        back_button = MDButton(
            MDButtonText(text="Back Home"),
            style="filled",
            size_hint=(0.5, 1),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.go_back
        )

        buttons_row.add_widget(clear_button)
        buttons_row.add_widget(back_button)

        content.add_widget(buttons_row)
        self.root_box.add_widget(content)

    def on_enter(self):
        self.update_cart()

    def update_cart(self):
        self.items_box.clear_widgets()
        total = 0

        for product in self.cart:
            self.items_box.add_widget(
                CartItemCard(product, self.remove_item)
            )
            total += product["price"]

        if not self.cart:
            self.items_box.add_widget(
                MDLabel(
                    text="Your cart is empty",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["muted"],
                    size_hint=(1, None),
                    height=dp(60)
                )
            )

        self.total_label.text = f"Total: {total} NIS"

    def remove_item(self, product):
        self.cart.remove(product)
        self.update_cart()

    def clear_cart(self, *args):
        self.cart.clear()
        self.update_cart()

    def go_back(self, *args):
        self.manager.current = "home"