from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from services.firebase_service import FirebaseService

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.name_input = TextInput(hint_text='Name')
        self.phone_input = TextInput(hint_text='Phone Number')
        self.age_input = TextInput(hint_text='Age')
        self.disability_input = TextInput(hint_text='Disability')
        self.nationality_input = TextInput(hint_text='Nationality')
        self.submit_button = Button(text='Submit', on_press=self.submit)

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.phone_input)
        self.layout.add_widget(self.age_input)
        self.layout.add_widget(self.disability_input)
        self.layout.add_widget(self.nationality_input)
        self.layout.add_widget(self.submit_button)

    def submit(self, instance):
        user_data = {
            'name': self.name_input.text,
            'phone': self.phone_input.text,
            'age': self.age_input.text,
            'disability': self.disability_input.text,
            'nationality': self.nationality_input.text
        }
        FirebaseService().save_user_data(user_data)