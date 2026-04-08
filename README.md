# Fauor Market Mobile

A mobile supermarket app project built with Python.

## Project Goal
Build a supermarket mobile app for Fauor Market while improving Python and GitHub skills.

# * * * SPLASH-SCREEN CLASS * * 

Clock.schedule_once(self.go_to_login, 2)
---> this means wait 2 seconds and then move the home screen 


# * * * LOGIN SCREEN CLASS * * *
* user name : admin
* password : 1234 
we can change the user name & the password for login here !
<if username == "admin" and password == "1234":>


# * * * PRODUCTS_SCREEN CLASS * * 

# Product information distribution
  - name
  - price
  - category
  - "add" button

# scrollview : This allows scrolling if there are many products: 
scroll_view = ScrollView(size_hint=(1, 1))

# This gives real control over the height of components:
size_hint=(1, None) + height=dp(...)
# example:
height=dp(120)

# buttons color:
background_normal=""
background_color=(0.1, 0.5, 0.8, 1)