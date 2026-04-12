from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
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


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
                text="My Profile",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"]
            )
        )

        self.root_box.add_widget(top_bar)

        scroll = ScrollView(size_hint=(1, 1))

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(14),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        self.profile_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(14),
            size_hint=(1, None),
            radius=[28, 28, 28, 28],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"]
        )
        self.profile_card.bind(minimum_height=self.profile_card.setter("height"))

        content.add_widget(self.profile_card)
        scroll.add_widget(content)
        self.root_box.add_widget(scroll)

    def on_enter(self):
        self.update_profile()

    def update_profile(self):
        self.profile_card.clear_widgets()

        app = MDApp.get_running_app()
        user = app.current_user

        if not user:
            self.profile_card.add_widget(
                MDLabel(
                    text="No user data available",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["muted"],
                    size_hint=(1, None),
                    height=dp(40)
                )
            )
            return

        title = MDLabel(
            text=f"{user['first_name']} {user['last_name']}",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Headline",
            role="small",
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )

        subtitle = MDLabel(
            text="Account Details",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large",
            size_hint=(1, None),
            height=dp(30)
        )

        self.profile_card.add_widget(title)
        self.profile_card.add_widget(subtitle)

        details = [
            ("First Name", user["first_name"]),
            ("Last Name", user["last_name"]),
            ("City", user["city"]),
            ("Home Location", user["home_location"] or "Not provided"),
            ("Phone", user["phone"]),
            ("Email", user["email"] or "Not provided"),
            ("Gender", user["gender"]),
            ("Username", user["username"]),
        ]

        for label_text, value_text in details:
            row = MDCard(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(4),
                size_hint=(1, None),
                radius=[18, 18, 18, 18],
                style="filled",
                md_bg_color=APP_COLORS["background"],
                line_color=APP_COLORS["border"],
            )
            row.bind(minimum_height=row.setter("height"))

            label = MDLabel(
                text=label_text,
                theme_text_color="Custom",
                text_color=APP_COLORS["accent"],
                font_style="Label",
                role="large",
                size_hint=(1, None),
                height=dp(24)
            )

            value = MDLabel(
                text=str(value_text),
                theme_text_color="Custom",
                text_color=APP_COLORS["text"],
                font_style="Body",
                role="large",
                size_hint=(1, None),
                height=dp(30)
            )

            row.add_widget(label)
            row.add_widget(value)
            self.profile_card.add_widget(row)

        back_button = MDButton(
            MDButtonText(text="Back Home"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.go_back
        )

        
        edit_button = MDButton(
            MDButtonText(text="Edit Profile"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_to_edit_profile
        )
        
        self.profile_card.add_widget(edit_button)
        self.profile_card.add_widget(back_button)
        
    def go_back(self, *args):
        self.manager.current = "home"
        
    def go_to_edit_profile(self, *args):
        self.manager.current = "edit_profile"