import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)

        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_finger_tip(self, hand_index=0, finger_id=8, frame_shape=(480,640,3)):
        if self.results.multi_hand_landmarks:
            handLms = self.results.multi_hand_landmarks[hand_index]
            h, w, _ = frame_shape
            lm = handLms.landmark[finger_id]
            return int(lm.x * w), int(lm.y * h), handLms
        return None, None, None
