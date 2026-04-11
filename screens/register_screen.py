from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText

from ui.theme import APP_COLORS
from services.db_service import create_user


class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.md_bg_color = APP_COLORS["background"]

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(18)
        )

        root.add_widget(MDBoxLayout())

        register_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(470),
            padding=dp(22),
            spacing=dp(18),
            radius=[28, 28, 28, 28],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"]
        )

        title = MDLabel(
            text="Register",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Headline",
            role="small",
            bold=True
        )

        subtitle = MDLabel(
            text="Create your account",
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

        self.confirm_input = MDTextField(
            hint_text="Confirm Password",
            mode="outlined",
            password=True,
            size_hint=(1, None),
            height=dp(56)
        )

        register_button = MDButton(
            MDButtonText(text="Create Account"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.register_user
        )

        login_button = MDButton(
            MDButtonText(text="Back to Login"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_to_login
        )
       

        self.message_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_style="Body",
            role="medium"
        )

        register_card.add_widget(title)
        register_card.add_widget(subtitle)
        register_card.add_widget(self.username_input)
        register_card.add_widget(self.password_input)
        register_card.add_widget(self.confirm_input)
        register_card.add_widget(register_button)
        register_card.add_widget(login_button)
        register_card.add_widget(self.message_label)
        
        root.add_widget(register_card)
        root.add_widget(MDBoxLayout())

        self.add_widget(root)

    def register_user(self, *args):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_input.text.strip()

        if not username or not password:
            self.message_label.text = "Please fill all fields"
            return

        if password != confirm:
            self.message_label.text = "Passwords do not match"
            return

        success = create_user(username, password)

        if success:
            self.message_label.text = "Account created successfully"
        else:
            self.message_label.text = "Username already exists"

    def go_to_login(self, *args):
        self.manager.current = "login"