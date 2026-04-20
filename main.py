from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FadeTransition
from screens.splash_screen import SplashScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.products_screen import ProductsScreen
from screens.cart_screen import CartScreen
from ui.theme import APP_COLORS
from screens.checkout_screen import CheckoutScreen
from services.db_service import create_tables, insert_products
from services.data_service import load_products
from screens.register_screen import RegisterScreen
from screens.profile_screen import ProfileScreen
from screens.edit_profile_screen import EditProfileScreen
from services.session_service import load_session
from services.db_service import get_user
from screens.order_history_screen import OrderHistoryScreen

class FauorApp(MDApp):
    def build(self):
        create_tables()
        insert_products(load_products())
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        # save the current user in the app instance for easy access across screens
        self.current_user = None
        
        cart = []
        # setting up the screen manager with all screens
        # using fade transition for smooth screen changes
        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(EditProfileScreen(name="edit_profile"))
        sm.add_widget(ProductsScreen(cart=cart, name="products"))
        sm.add_widget(CartScreen(cart=cart, name="cart"))
        sm.add_widget(CheckoutScreen(cart=cart, name="checkout"))
        sm.add_widget(OrderHistoryScreen(name="order_history"))
        
        saved_user = load_session()

        if saved_user:
            self.current_user = get_user(saved_user)
            sm.current = "home"
        else:
            sm.current = "splash"
            
        return sm


if __name__ == "__main__":
    FauorApp().run()