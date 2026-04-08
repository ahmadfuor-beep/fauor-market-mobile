from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.go_to_login, 2)

    def go_to_login(self, dt):
        self.manager.current = "login"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        title_label = Label(
            text="Fauor Market",
            font_size=40
        )

        subtitle_label = Label(
            text="Welcome to our supermarket app",
            font_size=20
        )

        layout.add_widget(title_label)
        layout.add_widget(subtitle_label)

        self.add_widget(layout)