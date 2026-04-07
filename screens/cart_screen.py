from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
################################################################
class CartScreen(Screen):
    def __init__(self, cart, **kwargs):
        super().__init__(**kwargs)
        self.cart = cart

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
            orientation="vertical",
            spacing=10
        )

        self.layout.add_widget(self.cart_items_layout)

        self.total_label = Label(
            text="Total: 0 NIS",
            font_size=20,
            size_hint=(1, 0.2)
        )

        self.layout.add_widget(self.total_label)
        
        clear_button = Button(
            text="Clear Cart",
            size_hint=(1, 0.2)
        )
        clear_button.bind(on_press=self.clear_cart)
        self.layout.add_widget(clear_button)

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

        for product in self.cart:
            item_box = BoxLayout(size_hint=(1, None), height=50, spacing=10)

            item_label = Label(
                text=f"{product['name']} - {product['price']} NIS"
            )
            
            remove_button = Button(
                text="Remove",
                size_hint=(0.3, 1)
            )

            remove_button.bind(
                on_press=lambda instance, p=product: self.remove_item(p)
            )
            item_box.add_widget(item_label)
            item_box.add_widget(remove_button)

            self.cart_items_layout.add_widget(item_box)
            
            total += product["price"]

        self.total_label.text = f"Total: {total} NIS"

    def remove_item(self, product):
        self.cart.remove(product)
        self.update_cart()

    def clear_cart(self, instance):
        self.cart.clear()
        self.update_cart()
    def go_back(self, instance):
        self.manager.current = "home"