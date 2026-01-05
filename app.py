import os, time
from flask import Flask, render_template, Response, jsonify, send_from_directory
import cv2
from emotion_model import infer_emotion_from_frame

# Emotion classes
CLASS_LIST = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

app = Flask(__name__, static_folder='static')

# ----------------------------------------------------------
# MUSIC LOADING
# ----------------------------------------------------------
def collect_music():
    catalog = {}
    base = os.path.join("static", "music")

    for emotion in CLASS_LIST:
        file_path = os.path.join(base, f"{emotion}.mp3")
        if os.path.exists(file_path):
            catalog[emotion] = [f"static/music/{emotion}.mp3"]
        else:
            catalog[emotion] = []

    return catalog


MUSIC = collect_music()

# ----------------------------------------------------------
# CAMERA
# ----------------------------------------------------------
cap = None

def open_camera():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)

        # FULL QUALITY CAMERA
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def close_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None


# ----------------------------------------------------------
# GLOBAL LAST PREDICTION
# ----------------------------------------------------------
last_pred = {
    "emotion": "neutral",
    "confidence": 0.0,
    "ts": 0.0,
    "res": None,
    "annotated_frame": None
}

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    "haarcascade_frontalface_default.xml")


def draw_box(frame, res):
    if res and "region" in res:
        r = res["region"]
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, res.get("dominant_emotion", ""), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        # fallback Haar detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        if len(faces) > 0:
            x, y, w, h = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame


# ----------------------------------------------------------
# MJPEG STREAM
# ----------------------------------------------------------
def gen_frames():
    global cap, last_pred

    open_camera()

    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        now = time.time()

        # Run emotion approx every 1 second
        if now - last_pred["ts"] > 0.9:
            emo, conf, res = infer_emotion_from_frame(frame)

            if emo:
                last_pred["emotion"] = emo
                last_pred["confidence"] = conf
                last_pred["res"] = res
            else:
                last_pred["emotion"] = "no face detected"
                last_pred["res"] = None

            last_pred["ts"] = now

        # Annotate frame
        annotated = frame.copy()
        annotated = draw_box(annotated, last_pred["res"])
        last_pred["annotated_frame"] = annotated.copy()

        ret, buffer = cv2.imencode(".jpg", annotated)
        if not ret:
            continue

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               buffer.tobytes() +
               b"\r\n")


# ----------------------------------------------------------
# ROUTES
# ----------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", class_list=CLASS_LIST)


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/status")
def status():
    em = last_pred["emotion"]
    tracks = MUSIC.get(em, [])
    return jsonify({"emotion": em, "tracks": tracks})


@app.route("/capture")
def capture():
    frame = last_pred.get("annotated_frame")
    emotion = last_pred.get("emotion", "neutral")

    if frame is None:
        return jsonify({"ok": False, "error": "no_frame"})

    save_path = os.path.join("static", "captures", "latest.jpg")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cv2.imwrite(save_path, frame)

    tracks = MUSIC.get(emotion, [])

    return jsonify({
        "ok": True,
        "emotion": emotion,
        "path": "static/captures/latest.jpg",
        "tracks": tracks
    })


@app.route("/music/<path:filename>")
def music(filename):
    return send_from_directory("static/music", filename)


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == "__main__":
    open_camera()
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    close_camera()
