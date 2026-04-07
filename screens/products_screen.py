from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from services.data_service import load_products
##############################################################
class ProductsScreen(Screen):
    def __init__(self,cart, **kwargs):
        super().__init__(**kwargs)
        self.cart = cart

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title_label = Label(
            text="Products",
            font_size=30,
            size_hint=(1, 0.2)
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
        self.cart.append(product)
        print(f"Added to cart: {product['name']}")
        print(self.cart)


    def go_back(self, instance):
        self.manager.current = "home"