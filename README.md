# Emotion-Aware Music Recommender Leveraging Facial Expressions

Built an emotion recognition model leveraging transfer learning with ResNet50 and the DeepFace framework. The system performs face detection, feature extraction, and emotion classification in real time. Integrated preprocessing, data augmentation, model evaluation, and Flask-based interface support.

This project detects human facial emotions using deep learning and automatically plays music based on the detected emotion. The model uses **ResNet50** and the **DeepFace** framework for emotion recognition and integrates a simple music player.

This work was developed as part of my **final year B.Tech Computer Science capstone project**.

---

## 🎥 Project Demo Video

👉 Watch the demo here:  
**[Add your video link here]**

---

## 🧠 Features

- Real-time emotion detection using webcam
- Uses **ResNet50** backbone via DeepFace
- Detects emotions such as:
  - Happy
  - Sad
  - Angry
  - Neutral
  - Fear
  - Surprise
- Maps each emotion to a corresponding song
- Simple Python implementation

---

## 🧰 Tech Stack

- Python
- DeepFace
- ResNet50
- OpenCV
- TensorFlow / Keras
- Flask (for UI if web version used)

---

## 🚀 How It Works (High Level)

1. Capture face using webcam
2. Detect and crop face region
3. Predict emotion using ResNet50 + DeepFace
4. Match emotion to predefined song
5. Play song automatically

---

## 📂 Project Contents

- `app.py` – main program
- `emotion_model.py` – model loading and prediction
- `templates/` – HTML interface
- `static/` – JS, CSS, images
- `upload_app/` – optional upload-based emotion detector
- Jupyter notebook – training / experimentation

> Note: Large files (trained models, songs, and datasets) are not uploaded to GitHub to keep the repository lightweight.

---

## 🙏 Acknowledgements

- FER2013 Dataset
- RAF-DB Dataset
- DeepFace Framework
- ResNet50 pre-trained weights

---

## 📜 Academic Use

This project is intended for **educational and research purposes** only.

