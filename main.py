from components.eye_tracking_keyboard import EyeTrackingKeyboard
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from components.login import LoginPage
from components.accessibility_eye_tracker import AccessibilityEyeTracker, EyeTracker
from components.sign_language import SignLanguage
from components.voice_to_text import VoiceToText

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(AccessibilityEyeTracker(name='eye_tracker'))
        sm.add_widget(SignLanguage(name='sign_language'))
        sm.add_widget(VoiceToText(name='voice_to_text'))
        sm.add_widget(EyeTrackingKeyboard(name='eye_tracking_keyboard'))
        return sm

if __name__ == '__main__':
    MainApp().run()