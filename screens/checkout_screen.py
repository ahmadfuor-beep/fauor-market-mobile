from kivy.metrics import dp
from kivy.animation import Animation
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
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from ui.theme import APP_COLORS
from services.db_service import clear_cart_db, get_cart_db, create_order

class CheckoutScreen(MDScreen):
    def __init__(self, cart, **kwargs):
        super().__init__(**kwargs)
        self.cart = cart
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
                text="Checkout",
                theme_text_color="Custom",
                text_color=APP_COLORS["text"]
            )
        )

        self.root_box.add_widget(top_bar)

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(14)
        )

        title_label = MDLabel(
            text="Order Summary",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["text"],
            font_style="Headline",
            role="small",
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )
        content.add_widget(title_label)

        self.summary_card = MDCard(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
            radius=[26, 26, 26, 26],
            style="filled",
            md_bg_color=APP_COLORS["surface"],
            line_color=APP_COLORS["border"]
        )
        content.add_widget(self.summary_card)

        self.total_label = MDLabel(
            text="Total: 0 NIS",
            halign="center",
            theme_text_color="Custom",
            text_color=APP_COLORS["accent"],
            font_style="Title",
            role="large",
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )
        content.add_widget(self.total_label)
        # store the original button color for later use in animation
        self.original_button_color = APP_COLORS["accent"]
        
        self.confirm_button = MDButton(
            MDButtonText(text="Confirm Order"),
            style="filled",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            md_bg_color=APP_COLORS["accent"],
            theme_bg_color="Custom",
            on_release=self.confirm_order
        )

        back_button = MDButton(
            MDButtonText(text="Back to Cart"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48),
            radius=[22, 22, 22, 22],
            line_color=APP_COLORS["border"],
            on_release=self.go_back
        )

        content.add_widget(self.confirm_button)
        content.add_widget(back_button)

        self.root_box.add_widget(content)

    def on_enter(self):
        self.update_summary()

    def update_summary(self):
        self.summary_card.clear_widgets()

        total = 0
        self.cart = get_cart_db()
        
        if not self.cart:
            self.summary_card.add_widget(
                MDLabel(
                    text="Your cart is empty",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["muted"],
                    size_hint=(1, None),
                    height=dp(40)
                )
            )
        else:
            for product in self.cart:
                row = MDLabel(
                    text=f"{product['name']} - {product['price']} NIS",
                    theme_text_color="Custom",
                    text_color=APP_COLORS["text"],
                    font_style="Body",
                    role="large",
                    size_hint=(1, None),
                    height=dp(32)
                )
                self.summary_card.add_widget(row)
                total += product["price"]

        self.total_label.text = f"Total: {total} NIS"

    def confirm_order(self, *args):
        if not self.cart:
            snackbar = MDSnackbar(
                MDSnackbarText(text="Your cart is empty")
            )
            snackbar.open()
            return

        app = MDApp.get_running_app()

        self.confirm_button.theme_bg_color = "Custom"
        self.confirm_button.md_bg_color = [0.2, 0.7, 0.3, 1]

        if app.current_user:
            create_order(app.current_user["username"], self.cart)

        anim = Animation(opacity=0, duration=0.35)
        anim.bind(on_complete=self.finish_order_animation)
        anim.start(self.summary_card)

        Animation(
            md_bg_color=self.original_button_color,
            duration=0.6
        ).start(self.confirm_button)
        
    def finish_order_animation(self, *args):
        clear_cart_db()
        self.cart.clear()

        self.summary_card.opacity = 1
        self.update_summary()

        snackbar = MDSnackbar(
            MDSnackbarText(text="Order confirmed successfully")
        )
        snackbar.open()
        
        
        
        
    def go_back(self, *args):
        self.manager.current = "cart"