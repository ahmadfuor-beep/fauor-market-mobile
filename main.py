#   import Files
import json
import os
#*************************************************************#
#Import from lIbraries
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
#*************************************************************#

#Function to load products from JSON file
def load_products():
    file_path = os.path.join(os.path.dirname(__file__), "data", "products.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
           orientation='vertical',
        padding =20,
        spacing = 15
        ) 
        title_label = Label(
           text='Fauor Market',
           font_size=32
       )
        welcome_label = Label(
           text='Welcome to Fauor Market!',
           font_size=20
       )
        products_button = Button(
           text='View Products',
           size_hint=(1, 0.2)
       )
        cart_button = Button(
           text = 'My Cart',
           size_hint=(1, 0.2)    
       )
        exit_button = Button(
              text = 'Exit',
              size_hint=(1, 0.2)
       )
       
        products_button.bind(on_press=self.go_to_products)
        exit_button.bind(on_press=self.close_app)

        layout.add_widget(title_label)
        layout.add_widget(welcome_label)
        layout.add_widget(products_button)
        layout.add_widget(cart_button)
        layout.add_widget(exit_button)
       
        self.add_widget(layout)
        #function to switch to products screen
    def go_to_products(self, instance):
        # Switch to the products screen
        self.manager.current = "products"

    def close_app(self, instance):
        App.get_running_app().stop()

class ProductsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title_label = Label(
            text="Products",
            font_size=30
        )
        layout.add_widget(title_label)

        products = load_products()
        
        for product in products:
            product_label = Label(text=f"{product['name']} - {product['price']:.2f} NIS")
            layout.add_widget(product_label)

        back_button = Button(
            text="Back to Home",
            size_hint=(1, 0.2)
        )
        
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "home"


class FauorApp(App):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(ProductsScreen(name="products"))

        return screen_manager

    
if __name__ == "__main__":
    FauorApp().run()
      