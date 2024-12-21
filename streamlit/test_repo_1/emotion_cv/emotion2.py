import cv2
from fer import FER

detector = FER()

def Get_Confidence(frame):

    emotions = ()

    emotion_predictions = detector.detect_emotions(frame)
    for face in emotion_predictions:
        emotion = max(face['emotions'], key=face['emotions'].get)
        emotions = (emotion,face["emotions"][emotion])

    return emotions
