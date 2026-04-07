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
# cart to store selected products
cart = []
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
        #
        cart_button.bind(on_press=self.go_to_cart)
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
        #function to switch to cart screen
    def go_to_cart(self, instance):
        self.manager.current = "cart"

class ProductsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title_label = Label(
            text="Products",
            font_size=30
        )
        self.layout.add_widget(title_label)

        self.load_products_ui()
        
        back_button = Button(
            text="Back to Home",
            size_hint=(1, 0.2)
        )
        
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)
        

    def load_products_ui(self):
        products = load_products()

        for product in products:
            product_box = BoxLayout(size_hint=(1, 0.2))

            product_label = Label(
                text=f"{product['name']} - {product['price']} NIS"
            )

            add_button = Button(
                text="Add",
                size_hint=(0.3, 1)
            )

            add_button.bind(
                on_press=lambda instance, p=product: self.add_to_cart(p)
            )

            product_box.add_widget(product_label)
            product_box.add_widget(add_button)

            self.layout.add_widget(product_box)

    def add_to_cart(self, product):
        cart.append(product)
        print(f"Added to cart: {product['name']}")

    def go_back(self, instance):
        self.manager.current = "home"
########### class for cart screen ##########
class CartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.title_label = Label(
            text="My Cart",
            font_size=30,
            size_hint=(1, 0.2)
        )

        self.layout.add_widget(self.title_label)

        self.cart_items_layout = BoxLayout(
            orientation="vertical"
        )

        self.layout.add_widget(self.cart_items_layout)

        self.total_label = Label(
            text="Total: 0 NIS",
            font_size=20,
            size_hint=(1, 0.2)
        )

        self.layout.add_widget(self.total_label)

        back_button = Button(
            text="Back to Home",
            size_hint=(1, 0.2)
        )

        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_cart()
    #function to update cart items and total price
    def update_cart(self):
        self.cart_items_layout.clear_widgets()

        total = 0

        for product in cart:
            item_label = Label(
                text=f"{product['name']} - {product['price']} NIS"
            )
            self.cart_items_layout.add_widget(item_label)

            total += product["price"]

        self.total_label.text = f"Total: {total} NIS"

    def go_back(self, instance):
        self.manager.current = "home"
########### class for running the app ##########
class FauorApp(App):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(ProductsScreen(name="products"))
        screen_manager.add_widget(CartScreen(name="cart"))
        return screen_manager

    
if __name__ == "__main__":
    FauorApp().run()
      