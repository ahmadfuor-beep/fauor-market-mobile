from kivy.clock import Clock
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

from ui.theme import APP_COLORS


class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.md_bg_color = APP_COLORS["background"]

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(24)
        )

        root.add_widget(MDBoxLayout())

        card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(260),
            padding=dp(24),
            spacing=dp(18),
            radius=[30, 30, 30, 30],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"]
        )

        title = MDLabel(
            text="Fauor Market",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Display",
            role="small",
            bold=True
        )

        subtitle = MDLabel(
            text="Smart shopping made simple",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["muted"],
            font_style="Body",
            role="large"
        )

        card.add_widget(title)
        card.add_widget(subtitle)

        root.add_widget(card)
        root.add_widget(MDBoxLayout())

        self.add_widget(root)

    def on_enter(self):
        Clock.schedule_once(self.go_to_login, 2)

    def go_to_login(self, dt):
        self.manager.current = "login"