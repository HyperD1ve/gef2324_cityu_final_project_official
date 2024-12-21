import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("emotion_cv/shape_predictor_68_face_landmarks.dat")

def Get_Keypoint(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if faces[0]:
        face = faces[0]
        landmarks = predictor(gray, face)
        return np.array([[p.x, p.y] for p in landmarks.parts()])
            

def Get_Confidence(frame):
    Points = Get_Keypoint(frame)
    emotion,confidence = Analyze_Confidence(Points)
    return emotion,confidence

def Analyze_Confidence(keypoints):
    if keypoints.shape != (68, 2):
        raise ValueError("Keypoints must be a numpy array of shape (68, 2)")

    left_eye = keypoints[36:42]  # Left eye landmarks
    right_eye = keypoints[42:48]  # Right eye landmarks
    mouth = keypoints[48:60]  # Mouth landmarks

    eye_distance = np.linalg.norm(np.mean(left_eye, axis=0) - np.mean(right_eye, axis=0))
    mouth_height = np.linalg.norm(mouth[3] - mouth[9])  # Distance between corners of the mouth

    emotion = "Neutral"
    confidence = 0.8

    if mouth_height > eye_distance * 0.5:
        emotion = "Confident"
        confidence = min(1.0, mouth_height / (eye_distance * 0.4))  # Confidence based on proportion
    elif mouth_height < eye_distance * 0.25:
        emotion = "Confuse"
        confidence = min(0.65, (eye_distance * 0.3 - mouth_height) / (eye_distance * 0.3))  # Confidence based on proportion

    confidence = round(confidence, 2)  # Round to two decimal places

    return emotion, confidence

