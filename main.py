from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button




class FauorApp(App):
    def build(self):
       main_layout = BoxLayout(
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
       
       exit_button.bind(on_press=self.close_app)

       main_layout.add_widget(title_label)
       main_layout.add_widget(welcome_label)
       main_layout.add_widget(products_button)
       main_layout.add_widget(cart_button)
       main_layout.add_widget(exit_button)

       return main_layout
    def close_app(self, instance):
     App.get_running_app().stop()
    
if __name__ == "__main__":
    FauorApp().run()
      