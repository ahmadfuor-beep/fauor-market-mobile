from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from ui.theme import APP_COLORS
from kivy.metrics import dp


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.md_bg_color = APP_COLORS["background"]

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(18)
        )

        root.add_widget(MDBoxLayout())

        login_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(420),
            padding=dp(22),
            spacing=dp(18),
            radius=[28, 28, 28, 28],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"]
        )

        title = MDLabel(
            text="Login",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Headline",
            role="small",
            bold=True
        )

        subtitle = MDLabel(
            text="Enter your account details",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large"
        )

        self.username_input = MDTextField(
            hint_text="Username",
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )

        self.password_input = MDTextField(
            hint_text="Password",
            mode="outlined",
            password=True,
            size_hint=(1, None),
            height=dp(56)
        )

        login_button = MDButton(
            MDButtonText(text="Login"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.check_login
        )

        self.message_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_style="Body",
            role="medium"
        )

        login_card.add_widget(title)
        login_card.add_widget(subtitle)
        login_card.add_widget(self.username_input)
        login_card.add_widget(self.password_input)
        login_card.add_widget(login_button)
        login_card.add_widget(self.message_label)

        root.add_widget(login_card)
        root.add_widget(MDBoxLayout())

        self.add_widget(root)

    def check_login(self, *args):
        username = self.username_input.text
        password = self.password_input.text

        if username == "admin" and password == "1234":
            self.message_label.text = "Login successful"
            self.manager.current = "home"
        else:
            self.message_label.text = "Invalid username or password"