from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from ui.theme import APP_COLORS
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.md_bg_color = APP_COLORS["background"]

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(18)
        )

        top_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(60)
        )

        top_row.add_widget(MDBoxLayout())

        greeting_card = MDCard(
            size_hint=(0.7, 1),
            radius=[24, 24, 24, 24],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"],
            padding=dp(12)
        )

        greeting_label = MDLabel(
            text=self.get_greeting(),
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Title",
            role="medium",
            bold=True
        )

        greeting_card.add_widget(greeting_label)

        top_row.add_widget(greeting_card)
        top_row.add_widget(MDBoxLayout())

        title_label = MDLabel(
            text="Fauor Market",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Display",
            role="small",
            bold=True
        )

        self.welcome_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Headline",
            role="medium",
            bold=True,
            size_hint=(1, None),
            height=dp(50)
        )

        menu_card = MDCard(
            orientation="vertical",
            radius=[28, 28, 28, 28],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"],
            padding=dp(20),
            spacing=dp(16)
        )

        products_button = MDButton(
            MDButtonText(text="View Products"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.go_to_products
        )

        cart_button = MDButton(
            MDButtonText(text="My Cart"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_to_cart
        )

        exit_button = MDButton(
            MDButtonText(text="Close App"),
            style="text",
            size_hint=(1, None),
            height=dp(42),
            on_release=self.close_app
        )

        menu_card.add_widget(products_button)
        menu_card.add_widget(cart_button)
        menu_card.add_widget(exit_button)

        root.add_widget(top_row)
        root.add_widget(title_label)
        root.add_widget(self.welcome_label)
        root.add_widget(menu_card)

        self.add_widget(root)

    def get_greeting(self):
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            return "Good Morning"
        elif 12 <= current_hour < 18:
            return "Good Afternoon"
        return "Good Evening"
    
    def on_enter(self):
        app = MDApp.get_running_app()

        if app.current_user:
            name = app.current_user["first_name"]
            self.welcome_label.text = f"Welcome {name} 👋"
        else:
            self.welcome_label.text = "Welcome 👋"

    def go_to_products(self, *args):
        self.manager.current = "products"

    def go_to_cart(self, *args):
        self.manager.current = "cart"

    def close_app(self, *args):
        MDApp.get_running_app().stop()