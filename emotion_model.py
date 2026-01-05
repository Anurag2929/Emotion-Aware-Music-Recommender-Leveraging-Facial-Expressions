from deepface import DeepFace
import cv2

CLASS_LIST = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def interpret(result):

    # DeepFace returns a list → first element is dict
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        result = result[0]

    # If emotion is dict
    if isinstance(result, dict) and isinstance(result.get("emotion"), dict):
        emo_dict = result["emotion"]
        emo = result.get("dominant_emotion", max(emo_dict, key=emo_dict.get))
        conf = float(emo_dict.get(emo, 0.0))
        return emo, conf

    return "neutral", 0.0


def pad(x, y, w, h, fw, fh, ratio=0.22):
    pw = int(w * ratio)
    ph = int(h * ratio)
    x1 = max(0, x - pw)
    y1 = max(0, y - ph)
    x2 = min(fw - 1, x + w + pw)
    y2 = min(fh - 1, y + h + ph)
    return x1, y1, x2 - x1, y2 - y1


def infer_emotion_from_frame(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)

        if len(faces) == 0:
            return None, 0.0, None

        x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]

        fh, fw = frame.shape[:2]
        x2, y2, w2, h2 = pad(x, y, w, h, fw, fh)
        roi = frame[y2:y2 + h2, x2:x2 + w2]

        result = DeepFace.analyze(
            roi,
            actions=["emotion"],
            detector_backend="opencv",
            enforce_detection=False
        )

        emo, conf = interpret(result)

        if not isinstance(result, dict):
            result = {}

        result["region"] = {"x": int(x2), "y": int(y2), "w": int(w2), "h": int(h2)}
        result["dominant_emotion"] = emo

        return emo, conf, result

    except Exception:
        return None, 0.0, None
