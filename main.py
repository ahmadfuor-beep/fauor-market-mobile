from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.home_screen import HomeScreen
from screens.products_screen import ProductsScreen
from screens.cart_screen import CartScreen

########### class for running the app ##########
class FauorApp(App):
    def build(self):
        cart = []
        
        screen_manager = ScreenManager()

        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(ProductsScreen(cart=cart, name="products"))
        screen_manager.add_widget(CartScreen(cart=cart, name="cart"))
        return screen_manager

    
if __name__ == "__main__":
    FauorApp().run()