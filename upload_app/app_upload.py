from flask import Flask, render_template, request
from deepface import DeepFace
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_predict():

    emotion_result = None
    uploaded_img_path = None

    if request.method == "POST":

        if "file" not in request.files:
            emotion_result = "No file uploaded"
            return render_template("index.html", emotion=emotion_result)

        file = request.files["file"]

        if file.filename == "":
            emotion_result = "No file selected"
            return render_template("index.html", emotion=emotion_result)

        # Save file
        uploaded_img_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(uploaded_img_path)

        try:
            # Run DeepFace
            result = DeepFace.analyze(
                img_path=uploaded_img_path, 
                actions=['emotion'],
                enforce_detection=False
            )

            # FIX: DeepFace returns a list inside v5
            if isinstance(result, list):
                result = result[0]

            dominant_emotion = result["dominant_emotion"]
            emotion_result = f"Detected Emotion: {dominant_emotion}"

        except Exception as e:
            emotion_result = f"Error: {str(e)}"

    return render_template("index.html",
                           emotion=emotion_result,
                           img_path=uploaded_img_path)


if __name__ == "__main__":
    app.run(debug=True)
