from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens.splash_screen import SplashScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.products_screen import ProductsScreen
from screens.cart_screen import CartScreen
from ui.theme import APP_COLORS
from screens.checkout_screen import CheckoutScreen

class FauorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"

        cart = []

        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProductsScreen(cart=cart, name="products"))
        sm.add_widget(CartScreen(cart=cart, name="cart"))
        sm.add_widget(CheckoutScreen(cart=cart, name="checkout"))
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    FauorApp().run()