
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
################################################################
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
           size_hint=(1, 0.2),
           background_normal="",
           background_color=(0.1, 0.6, 0.8, 1)
       )
        cart_button = Button(
           text = 'My Cart',
           size_hint=(1, 0.2),
           background_normal="",
           background_color=(0.2, 0.7, 0.3, 1)   
       )
        exit_button = Button(
              text = 'Exit',
              size_hint=(1, 0.2),
              background_normal="",
              background_color=(0.8, 0.2, 0.2, 1)
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