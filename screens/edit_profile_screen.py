from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
    MDTopAppBarLeadingButtonContainer,
    MDActionTopAppBarButton,
)

from ui.theme import APP_COLORS
from services.db_service import update_user, get_user


class EditProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.md_bg_color = APP_COLORS["background"]

        self.root_box = MDBoxLayout(orientation="vertical")
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
                text="Edit Profile",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"]
            )
        )
        self.root_box.add_widget(top_bar)

        scroll = ScrollView(size_hint=(1, 1))

        content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(16),
            padding=dp(16)
        )
        content.bind(minimum_height=content.setter("height"))

        self.form_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            padding=dp(20),
            spacing=dp(14),
            radius=[28, 28, 28, 28],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"]
        )
        self.form_card.bind(minimum_height=self.form_card.setter("height"))

        self.first_name_input = MDTextField(
            MDTextFieldHintText(text="First Name"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )
        self.last_name_input = MDTextField(
            MDTextFieldHintText(text="Last Name"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )
        self.city_input = MDTextField(
            MDTextFieldHintText(text="City"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )
        self.home_location_input = MDTextField(
            MDTextFieldHintText(text="Home Location"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )
        self.phone_input = MDTextField(
            MDTextFieldHintText(text="Phone Number"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )
        self.email_input = MDTextField(
            MDTextFieldHintText(text="Email"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )
        self.gender_input = MDTextField(
            MDTextFieldHintText(text="Gender"),
            mode="outlined",
            size_hint=(1, None),
            height=dp(56)
        )

        save_button = MDButton(
            MDButtonText(text="Save Changes"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.save_changes
        )

        cancel_button = MDButton(
            MDButtonText(text="Cancel"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_back
        )

        self.message_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            size_hint=(1, None),
            height=dp(36)
        )

        self.form_card.add_widget(self.first_name_input)
        self.form_card.add_widget(self.last_name_input)
        self.form_card.add_widget(self.city_input)
        self.form_card.add_widget(self.home_location_input)
        self.form_card.add_widget(self.phone_input)
        self.form_card.add_widget(self.email_input)
        self.form_card.add_widget(self.gender_input)
        self.form_card.add_widget(save_button)
        self.form_card.add_widget(cancel_button)
        self.form_card.add_widget(self.message_label)

        content.add_widget(self.form_card)
        scroll.add_widget(content)
        self.root_box.add_widget(scroll)

    def on_enter(self):
        app = MDApp.get_running_app()
        user = app.current_user

        if user:
            self.first_name_input.text = user["first_name"] or ""
            self.last_name_input.text = user["last_name"] or ""
            self.city_input.text = user["city"] or ""
            self.home_location_input.text = user["home_location"] or ""
            self.phone_input.text = user["phone"] or ""
            self.email_input.text = user["email"] or ""
            self.gender_input.text = user["gender"] or ""

    def save_changes(self, *args):
        app = MDApp.get_running_app()
        user = app.current_user

        if not user:
            self.message_label.text = "No user loaded"
            return

        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        city = self.city_input.text.strip()
        home_location = self.home_location_input.text.strip()
        phone = self.phone_input.text.strip()
        email = self.email_input.text.strip()
        gender = self.gender_input.text.strip()

        if not first_name or not last_name or not city or not phone or not gender:
            self.message_label.text = "Please fill all required fields"
            return

        update_user(
            user["username"],
            first_name,
            last_name,
            city,
            home_location,
            phone,
            email,
            gender
        )

        app.current_user = get_user(user["username"])
        self.message_label.text = "Profile updated successfully"

    def go_back(self, *args):
        self.manager.current = "profile"