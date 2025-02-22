import cv2
import dlib
from kivy.uix.screen import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from gtts import gTTS
import os

class SignLanguage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize dlib's face detector and shape predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download this file
        self.cap = cv2.VideoCapture(0)
        self.text_input = TextInput(hint_text='Detected Text', font_size=30, size_hint_y=None, height=100)
        self.backspace_button = Button(text='Backspace', on_press=self.backspace, size_hint_y=None, height=50)
        self.add_widget(self.text_input)
        self.add_widget(self.backspace_button)

        # Mapping of gestures to alphabets and numbers
        self.gesture_mappings = {
            "A": self.is_A,
            "B": self.is_B,
            "C": self.is_C,
            "D": self.is_D,
            "E": self.is_E,
            "F": self.is_F,
            "G": self.is_G,
            "H": self.is_H,
            "I": self.is_I,
            "J": self.is_J,
            "K": self.is_K,
            "L": self.is_L,
            "M": self.is_M,
            "N": self.is_N,
            "O": self.is_O,
            "P": self.is_P,
            "Q": self.is_Q,
            "R": self.is_R,
            "S": self.is_S,
            "T": self.is_T,
            "U": self.is_U,
            "V": self.is_V,
            "W": self.is_W,
            "X": self.is_X,
            "Y": self.is_Y,
            "Z": self.is_Z,
            "0": self.is_0,
            "1": self.is_1,
            "2": self.is_2,
            "3": self.is_3,
            "4": self.is_4,
            "5": self.is_5,
            "6": self.is_6,
            "7": self.is_7,
            "8": self.is_8,
            "9": self.is_9,
        }

    def detect_alphabet(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert frame to grayscale for dlib
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces (or hands) using dlib
        faces = self.detector(gray)
        for face in faces:
            # Get facial landmarks (can be adapted for hand landmarks)
            landmarks = self.predictor(gray, face)

            # Detect gesture based on landmarks
            detected_alphabet = self.detect_gesture(landmarks)
            if detected_alphabet:
                self.text_input.text += detected_alphabet
                self.read_aloud(detected_alphabet)

        # Display the frame
        cv2.imshow("Sign Language", frame)

    def detect_gesture(self, landmarks):
        # Check each gesture mapping
        for alphabet, check_gesture in self.gesture_mappings.items():
            if check_gesture(landmarks):
                return alphabet
        return None

    def read_aloud(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("mpg321 output.mp3")  # Use a suitable audio player

    def backspace(self, instance):
        self.text_input.text = self.text_input.text[:-1]

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    # Gesture detection methods for alphabets and numbers
    def is_A(self, landmarks):
        # Thumb folded over palm, other fingers extended
        thumb_tip = landmarks.part(4)  # Thumb tip landmark
        index_tip = landmarks.part(8)  # Index finger tip landmark
        return thumb_tip.y > index_tip.y

    def is_B(self, landmarks):
        # All fingers extended, thumb alongside palm
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return thumb_tip.y < index_tip.y

    def is_C(self, landmarks):
        # Hand forms a 'C' shape
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return abs(thumb_tip.x - index_tip.x) < 10  # Adjust threshold as needed

    def is_D(self, landmarks):
        # Index finger extended, other fingers folded
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y

    def is_E(self, landmarks):
        # All fingers folded into a fist
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return thumb_tip.y > index_tip.y

    def is_F(self, landmarks):
        # Index and thumb forming a circle, other fingers extended
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return abs(thumb_tip.x - index_tip.x) < 10 and abs(thumb_tip.y - index_tip.y) < 10

    def is_G(self, landmarks):
        # Index finger pointing, thumb alongside palm
        index_tip = landmarks.part(8)
        thumb_tip = landmarks.part(4)
        return index_tip.y < thumb_tip.y

    def is_H(self, landmarks):
        # Index and middle fingers extended, forming a 'V' shape
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y

    def is_I(self, landmarks):
        # Pinky finger extended, other fingers folded
        pinky_tip = landmarks.part(20)
        ring_tip = landmarks.part(16)
        return pinky_tip.y < ring_tip.y

    def is_J(self, landmarks):
        # Pinky finger extended with a circular motion
        pinky_tip = landmarks.part(20)
        ring_tip = landmarks.part(16)
        return pinky_tip.y < ring_tip.y

    def is_K(self, landmarks):
        # Index and middle fingers extended, thumb touching the base of the index finger
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        thumb_tip = landmarks.part(4)
        return index_tip.y < middle_tip.y and thumb_tip.y > index_tip.y

    def is_L(self, landmarks):
        # Index finger and thumb extended, forming an 'L' shape
        index_tip = landmarks.part(8)
        thumb_tip = landmarks.part(4)
        return index_tip.y < thumb_tip.y

    def is_M(self, landmarks):
        # All fingers folded, thumb tucked under the index finger
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return thumb_tip.y > index_tip.y

    def is_N(self, landmarks):
        # All fingers folded, thumb tucked under the middle finger
        thumb_tip = landmarks.part(4)
        middle_tip = landmarks.part(12)
        return thumb_tip.y > middle_tip.y

    def is_O(self, landmarks):
        # All fingers curled into a circle
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return abs(thumb_tip.x - index_tip.x) < 10 and abs(thumb_tip.y - index_tip.y) < 10

    def is_P(self, landmarks):
        # Index finger and thumb extended, forming a 'P' shape
        index_tip = landmarks.part(8)
        thumb_tip = landmarks.part(4)
        return index_tip.y < thumb_tip.y

    def is_Q(self, landmarks):
        # Index finger and thumb extended, forming a 'Q' shape
        index_tip = landmarks.part(8)
        thumb_tip = landmarks.part(4)
        return index_tip.y < thumb_tip.y

    def is_R(self, landmarks):
        # Index and middle fingers crossed
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y

    def is_S(self, landmarks):
        # Fist with thumb over fingers
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return thumb_tip.y > index_tip.y

    def is_T(self, landmarks):
        # Index finger extended, thumb touching the base of the index finger
        index_tip = landmarks.part(8)
        thumb_tip = landmarks.part(4)
        return index_tip.y < thumb_tip.y

    def is_U(self, landmarks):
        # Index and middle fingers extended, forming a 'U' shape
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y

    def is_V(self, landmarks):
        # Index and middle fingers extended, forming a 'V' shape
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y

    def is_W(self, landmarks):
        # Index, middle, and ring fingers extended, forming a 'W' shape
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        ring_tip = landmarks.part(16)
        return index_tip.y < middle_tip.y and middle_tip.y < ring_tip.y

    def is_X(self, landmarks):
        # Index finger bent, other fingers folded
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y > middle_tip.y

    def is_Y(self, landmarks):
        # Thumb and pinky finger extended, other fingers folded
        thumb_tip = landmarks.part(4)
        pinky_tip = landmarks.part(20)
        return thumb_tip.y < pinky_tip.y

    def is_Z(self, landmarks):
        # Index finger moving in a 'Z' shape
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y
    
    def is_0(self, landmarks):
        # Hand forms a circle
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return abs(thumb_tip.x - index_tip.x) < 10 and abs(thumb_tip.y - index_tip.y) < 10

    def is_1(self, landmarks):
        # Index finger extended
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        return index_tip.y < middle_tip.y

    def is_2(self, landmarks):
        # Index and middle fingers extended
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        ring_tip = landmarks.part(16)
        return index_tip.y < middle_tip.y and middle_tip.y < ring_tip.y

    def is_3(self, landmarks):
        # Index, middle, and ring fingers extended
        index_tip = landmarks.part(8)
        middle_tip = landmarks.part(12)
        ring_tip = landmarks.part(16)
        pinky_tip = landmarks.part(20)
        return index_tip.y < middle_tip.y and middle_tip.y < ring_tip.y and ring_tip.y < pinky_tip.y

    def is_4(self, landmarks):
        # All fingers extended except the thumb
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return thumb_tip.y > index_tip.y

    def is_5(self, landmarks):
        # All fingers extended
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return thumb_tip.y < index_tip.y

    def is_6(self, landmarks):
        # Thumb and pinky finger touching, other fingers extended
        thumb_tip = landmarks.part(4)
        pinky_tip = landmarks.part(20)
        return abs(thumb_tip.x - pinky_tip.x) < 10 and abs(thumb_tip.y - pinky_tip.y) < 10

    def is_7(self, landmarks):
        # Thumb and index finger touching, other fingers extended
        thumb_tip = landmarks.part(4)
        index_tip = landmarks.part(8)
        return abs(thumb_tip.x - index_tip.x) < 10 and abs(thumb_tip.y - index_tip.y) < 10

    def is_8(self, landmarks):
        # Thumb and middle finger touching, other fingers extended
        thumb_tip = landmarks.part(4)
        middle_tip = landmarks.part(12)
        return abs(thumb_tip.x - middle_tip.x) < 10 and abs(thumb_tip.y - middle_tip.y) < 10

    def is_9(self, landmarks):
        # Thumb and ring finger touching, other fingers extended
        thumb_tip = landmarks.part(4)
        ring_tip = landmarks.part(16)
        return abs(thumb_tip.x - ring_tip.x) < 10 and abs(thumb_tip.y - ring_tip.y) < 10