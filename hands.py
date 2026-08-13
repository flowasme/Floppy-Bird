import mediapipe.python.solutions.hands as hands
import mediapipe.python.solutions.drawing_utils as mp_draw
import cv2 as cv
import numpy as np

mp_hands = hands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv.CAP_PROP_FPS, 30)
w, h = 1280, 720

def process_frame():
    index_tip_coordinates = None
    success, frame = capture.read()
    if success:
        frame = cv.flip(frame, 1)
        RGBframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = mp_hands.process(RGBframe)
        if results.multi_hand_landmarks is not None:
            index_tip_coordinates = (int(results.multi_hand_landmarks[0].landmark[8].x * w), int(results.multi_hand_landmarks[0].landmark[8].y * h)) 
            cv.circle(frame, index_tip_coordinates, 10, (255, 0, 0), -1)
    return success, frame, index_tip_coordinates

def release_camera():
    capture.release()
    cv.destroyAllWindows()