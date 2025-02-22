import cv2
import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

class EyeTrackingKeyboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.add_widget(self.layout)

        # Text input display
        self.text_input = Label(text="", font_size=30, size_hint_y=None, height=100)
        self.layout.add_widget(self.text_input)

        # Keyboard layout
        self.keyboard_layout = GridLayout(cols=10, size_hint_y=None, height=300)
        self.layout.add_widget(self.keyboard_layout)

        # Add keys (numbers and alphabets)
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Backspace'
        ]
        self.keys = {}
        for key in keys:
            btn = Button(text=key, font_size=20)
            btn.bind(on_press=self.on_key_press)
            self.keyboard_layout.add_widget(btn)
            self.keys[key] = btn

        # Eye tracking setup
        self.cap = cv2.VideoCapture(0)
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.blink_counter = 0
        self.blink_threshold = 3  # Number of frames to detect a blink
        self.current_key = None

        # Start eye tracking
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update at 30 FPS

    def on_key_press(self, instance):
        """Handle key press events."""
        key = instance.text
        if key == 'Backspace':
            self.text_input.text = self.text_input.text[:-1]  # Remove last character
        else:
            self.text_input.text += key  # Add the key to the text input

    def update(self, dt):
        """Update eye tracking and blink detection."""
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert frame to grayscale for eye detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles around detected eyes
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Detect blink (simple logic: no eyes detected for a few frames)
        if len(eyes) == 0:
            self.blink_counter += 1
            if self.blink_counter == self.blink_threshold:
                self.handle_blink()
        else:
            self.blink_counter = 0

        # Display the frame
        cv2.imshow("Eye Tracking", frame)
        cv2.waitKey(1)

    def handle_blink(self):
        """Handle blink event (simulate key press)."""
        if self.current_key:
            self.on_key_press(self.keys[self.current_key])

    def on_enter(self):
        """Start video capture when the screen is entered."""
        self.cap = cv2.VideoCapture(0)

    def on_leave(self):
        """Release video capture when the screen is left."""
        self.cap.release()
        cv2.destroyAllWindows()

    def on_touch_down(self, touch):
        """Detect which key is being looked at based on touch position."""
        for key, btn in self.keys.items():
            if btn.collide_point(*touch.pos):
                self.current_key = key
                break