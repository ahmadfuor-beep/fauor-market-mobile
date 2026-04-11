from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
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
            padding=dp(20),
            spacing=dp(12),
        )

        scroll = ScrollView(size_hint=(1, 1))

        content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(16),
            padding=[0, dp(10), 0, dp(20)],
        )
        content.bind(minimum_height=content.setter("height"))

        register_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            padding=dp(22),
            spacing=dp(16),
            radius=[28, 28, 28, 28],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"],
        )
        register_card.bind(minimum_height=register_card.setter("height"))

        title = MDLabel(
            text="Create Your Account",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Headline",
            role="small",
            bold=True,
            size_hint=(1, None),
            height=dp(40),
        )

        subtitle = MDLabel(
            text="Fill in the required details below",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large",
            size_hint=(1, None),
            height=dp(30),
        )

        info_label = MDLabel(
            text="Required: first name, last name, city, phone, gender, username, password",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="small",
            size_hint=(1, None),
            height=dp(50),
        )

        self.first_name_input = MDTextField(
            MDTextFieldHintText(text="First Name (required)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.last_name_input = MDTextField(
            MDTextFieldHintText(text="Last Name (required)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.city_input = MDTextField(
            MDTextFieldHintText(text="City (required)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.home_location_input = MDTextField(
            MDTextFieldHintText(text="Home Location (optional)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.phone_input = MDTextField(
            MDTextFieldHintText(text="Phone Number (required)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.email_input = MDTextField(
            MDTextFieldHintText(text="Email Address (optional)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.gender_input = MDTextField(
            MDTextFieldHintText(text="Gender (required)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.username_input = MDTextField(
            MDTextFieldHintText(text="Username (required)"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56),
        )

        self.password_input = MDTextField(
            MDTextFieldHintText(text="Password (required)"),
            mode="outlined",
            password=True,
            size_hint=(1, None),
            height=dp(56),
        )

        self.confirm_input = MDTextField(
            MDTextFieldHintText(text="Confirm Password (required)"),
            mode="outlined",
            password=True,
            size_hint=(1, None),
            height=dp(56),
        )

        register_button = MDButton(
            MDButtonText(text="Create Account"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.register_user,
        )

        login_button = MDButton(
            MDButtonText(text="Back to Login"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_to_login,
        )

        self.message_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_style="Body",
            role="medium",
            size_hint=(1, None),
            height=dp(40),
        )

        register_card.add_widget(title)
        register_card.add_widget(subtitle)
        register_card.add_widget(info_label)
        register_card.add_widget(self.first_name_input)
        register_card.add_widget(self.last_name_input)
        register_card.add_widget(self.city_input)
        register_card.add_widget(self.home_location_input)
        register_card.add_widget(self.phone_input)
        register_card.add_widget(self.email_input)
        register_card.add_widget(self.gender_input)
        register_card.add_widget(self.username_input)
        register_card.add_widget(self.password_input)
        register_card.add_widget(self.confirm_input)
        register_card.add_widget(register_button)
        register_card.add_widget(login_button)
        register_card.add_widget(self.message_label)

        content.add_widget(register_card)
        scroll.add_widget(content)
        root.add_widget(scroll)

        self.add_widget(root)

    def register_user(self, *args):
        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        city = self.city_input.text.strip()
        home_location = self.home_location_input.text.strip()
        phone = self.phone_input.text.strip()
        email = self.email_input.text.strip()
        gender = self.gender_input.text.strip()
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_input.text.strip()

        if not first_name or not last_name or not city or not phone or not gender or not username or not password:
            self.message_label.text = "Please fill all required fields"
            return

        if password != confirm:
            self.message_label.text = "Passwords do not match"
            return

        success = create_user(
            first_name,
            last_name,
            city,
            home_location,
            phone,
            email,
            gender,
            username,
            password,
        )

        if success:
            self.message_label.text = "Account created successfully"
        else:
            self.message_label.text = "Username already exists"

    def go_to_login(self, *args):
        self.manager.current = "login"