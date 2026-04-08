from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title_label = Label(
            text="Login",
            font_size=32
        )

        self.username_input = TextInput(
            hint_text="Enter username",
            multiline=False
        )

        self.password_input = TextInput(
            hint_text="Enter password",
            multiline=False,
            password=True
        )

        login_button = Button(
            text="Login",
            size_hint=(1, 0.2),
            background_normal="",
            background_color=(0.1, 0.6, 0.8, 1)
        )

        self.message_label = Label(
            text="",
            font_size=18
        )

        login_button.bind(on_press=self.check_login)

        layout.add_widget(title_label)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(self.message_label)

        self.add_widget(layout)

    def check_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        # here we can chnage the "username" and "password" to any value we want to test the login functionality
        if username == "admin" and password == "1234":
            self.message_label.text = "Login successful"
            self.manager.current = "home"
        else:
            self.message_label.text = "Invalid username or password"