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
from services.db_service import get_orders_by_username, get_order_items


class OrderHistoryScreen(MDScreen):
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
                text="Order History",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"]
            )
        )

        self.root_box.add_widget(top_bar)

        scroll = ScrollView(size_hint=(1, 1))

        self.content = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(14),
            size_hint_y=None
        )
        self.content.bind(minimum_height=self.content.setter("height"))

        scroll.add_widget(self.content)
        self.root_box.add_widget(scroll)

    def on_enter(self):
        self.update_history()

    def update_history(self):
        self.content.clear_widgets()

        app = MDApp.get_running_app()
        user = app.current_user

        if not user:
            self.content.add_widget(
                MDLabel(
                    text="No user logged in",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["muted"],
                    size_hint=(1, None),
                    height=dp(50)
                )
            )
            return

        orders = get_orders_by_username(user["username"])

        if not orders:
            self.content.add_widget(
                MDLabel(
                    text="No orders yet",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["muted"],
                    size_hint=(1, None),
                    height=dp(50)
                )
            )
            return

        for order in orders:
            card = MDCard(
                orientation="vertical",
                padding=dp(16),
                spacing=dp(10),
                size_hint=(1, None),
                radius=[24, 24, 24, 24],
                style="filled",
                md_bg_color=APP_COLORS["surface"],
                line_color=APP_COLORS["border"]
            )
            card.bind(minimum_height=card.setter("height"))

            title = MDLabel(
                text=f"Order #{order['id']}",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"],
                font_style="Title",
                role="medium",
                bold=True,
                size_hint=(1, None),
                height=dp(30)
            )

            date_label = MDLabel(
                text=f"Date: {order['created_at']}",
                theme_text_color="Custom",
                text_color=APP_COLORS["muted"],
                font_style="Body",
                role="medium",
                size_hint=(1, None),
                height=dp(26)
            )

            total_label = MDLabel(
                text=f"Total: {order['total']} NIS",
                theme_text_color="Custom",
                text_color=APP_COLORS["accent"],
                font_style="Body",
                role="large",
                size_hint=(1, None),
                height=dp(28)
            )

            card.add_widget(title)
            card.add_widget(date_label)
            card.add_widget(total_label)

            items = get_order_items(order["id"])

            for item in items:
                item_label = MDLabel(
                    text=f"• {item['name']} - {item['price']} NIS",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["text"],
                    font_style="Body",
                    role="medium",
                    size_hint=(1, None),
                    height=dp(24)
                )
                card.add_widget(item_label)

            self.content.add_widget(card)

        back_button = MDButton(
            MDButtonText(text="Back Home"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            on_release=self.go_back
        )
        self.content.add_widget(back_button)

    def go_back(self, *args):
        self.manager.current = "home"