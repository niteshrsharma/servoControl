import cv2
import mediapipe as mp
import numpy as np
import serial
import time

arduinoPort=input("enter port: ")

arduino = serial.Serial(f'{arduinoPort}', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(distance, max_distance):
    angle = np.interp(distance, [0, max_distance], [0, 180])
    return angle

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x, 
                         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y]
            index_finger_tip = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, 
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y]
            distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_finger_tip))
            max_distance = 0.3
            angle = calculate_angle(distance, max_distance)
            arduino.write(f"{int(angle)}\n".encode())
            cv2.putText(frame, f'Angle: {int(angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('Hand Tracking', frame)
    time.sleep(0.05)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
