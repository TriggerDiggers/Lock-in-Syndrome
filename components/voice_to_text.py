import speech_recognition as sr
from kivy.uix.screen import Screen
from kivy.uix.label import Label

class VoiceToText(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recognizer = sr.Recognizer()
        self.label = Label(text="Recognized Text Will Appear Here")
        self.add_widget(self.label)

    def convert_to_text(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                self.label.text = text
            except sr.UnknownValueError:
                print("Could not understand audio")