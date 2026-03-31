from kivy.app import App
from kivy.uix.label import Label

class FauorApp(App):
    def build(self):
        return Label(text='Welcome to Fauor Market!')
if __name__ == '__main__':
    FauorApp().run()
      