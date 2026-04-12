from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from ui.theme import APP_COLORS
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.label import MDLabel, MDIcon

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.md_bg_color = APP_COLORS["background"]
        self.animations_started = False

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(18)
        )

        # top row with welcome and greeting
        top_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(66),
            spacing=dp(14)
        )

        #welcome card at the left
        self.user_card = MDCard(
            size_hint=(0.5, 1),
            radius=[22, 22, 22, 22],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"],
            padding=dp(12)
        )

        user_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10)
        )

        self.user_icon = MDIcon(
            icon="account-circle",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_size=dp(28),
            size_hint=(None, 1),
            width=dp(36)
        )

        self.user_label = MDLabel(
            text="Welcome",
            halign="left",
            valign="middle",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Body",
            role="large",
            bold=True
        )

        user_box.add_widget(self.user_icon)
        user_box.add_widget(self.user_label)

        self.user_card.add_widget(user_box)

        # greeting card at the right
        self.greeting_card = MDCard(
            size_hint=(0.5, 1),
            radius=[22, 22, 22, 22],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"],
            padding=dp(12)
        )

        greeting_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10)
        )

        self.greeting_icon = MDIcon(
            icon="weather-sunset-up",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_size=dp(28),
            size_hint=(None, 1),
            width=dp(36)
        )

        self.greeting_label = MDLabel(
            text=self.get_greeting(),
            halign="left",
            valign="middle",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Body",
            role="large",
            bold=True
        )

        greeting_box.add_widget(self.greeting_icon)
        greeting_box.add_widget(self.greeting_label)

        self.greeting_card.add_widget(greeting_box)

        top_row.add_widget(self.user_card)
        top_row.add_widget(self.greeting_card)

        title_label = MDLabel(
            text="Fauor Market",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Display",
            role="small",
            bold=True
        )

        subtitle_label = MDLabel(
            text="Welcome to our supermarket app",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large"
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

        profile_button = MDButton(
            MDButtonText(text="My Profile"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_to_profile
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
        menu_card.add_widget(profile_button)
        
        root.add_widget(top_row)
        root.add_widget(title_label)
        root.add_widget(subtitle_label)
        root.add_widget(menu_card)

        self.add_widget(root)

    def get_greeting(self):
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            return "Good Morning"
        elif 12 <= current_hour < 18:
            return "Good Afternoon"
        return "Good Evening"

    def start_icon_animations(self):
        user_anim = (
            Animation(opacity=0.5, duration=0.8) +
            Animation(opacity=1, duration=0.8)
        )
        user_anim.repeat = True
        user_anim.start(self.user_icon)

        greeting_anim = (
            Animation(font_size=dp(24), duration=0.8) +
            Animation(font_size=dp(28), duration=0.8)
        )
        greeting_anim.repeat = True
        greeting_anim.start(self.greeting_icon)

    def on_enter(self):
        app = MDApp.get_running_app()

        if app.current_user:
            name = app.current_user["first_name"].strip().title()
            self.user_label.text = f"Welcome {name}"
        else:
            self.user_label.text = "Welcome"

        current_greeting = self.get_greeting()
        self.greeting_label.text = current_greeting

        if "Morning" in current_greeting:
            self.greeting_icon.icon = "weather-sunny"
        elif "Afternoon" in current_greeting:
            self.greeting_icon.icon = "white-balance-sunny"
        else:
            self.greeting_icon.icon = "weather-night"

        if not getattr(self, "animations_started", False):
            self.start_icon_animations()
            self.animations_started = True

    def go_to_products(self, *args):
        self.manager.current = "products"

    def go_to_cart(self, *args):
        self.manager.current = "cart"
        
    def go_to_profile(self, *args):
        self.manager.current = "profile"

    def close_app(self, *args):
        MDApp.get_running_app().stop()