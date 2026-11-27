
# 🏀 COURTSIDE AI

### See the Game. Beyond the Game.

**AI-Powered Basketball Object Detection & Multi-Object Tracking**

Developed by **Mai Mohammed**

---

## 📌 Project Overview

COURTSIDE AI is an end-to-end computer vision application
designed to detect and track basketball-related objects
in images and videos using a fine-tuned YOLO26s model.

## 🚀 Features

- Basketball image detection
- Real-world video analysis
- Multi-object tracking using ByteTrack
- Adjustable confidence threshold
- Downloadable processed videos
- Premium interactive Streamlit interface

## 🎯 Detected Classes

- Basketball
- Field Goal Attempt
- Field Goal Made
- Hoop
- Player

## 📊 Model Performance

| Metric | Result |
|---|---:|
| Validation Precision | 93.9% |
| Validation Recall | 92.6% |
| Validation mAP50 | 95.6% |
| Validation mAP50-95 | 79.0% |
| Test mAP50 | 98.0% |
| Peak Test F1-Score | 96.0% |

## 🧠 Model Configuration

| Parameter | Value |
|---|---|
| Architecture | YOLO26s |
| Training Method | Fine-Tuning |
| Dataset Size | 8,452 Images |
| Training Images | 6,762 |
| Validation Images | 845 |
| Test Images | 845 |
| Epochs | 50 |
| Image Size | 640 × 640 |
| GPU | NVIDIA Tesla T4 |
| Model Size | 20.3 MB |

## 🛠️ Technologies

- Python
- PyTorch
- Ultralytics YOLO26
- OpenCV
- ByteTrack
- Streamlit
- FFmpeg
- Roboflow
- Kaggle

## 📂 Project Structure

```text
Basketball-Game-Analysis/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── hero.png
├── app.py
├── utils.py
├── best.pt
├── basketball_training.ipynb
├── requirements.txt
├── packages.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

Install FFmpeg and ensure it is available in your PATH.

Run the application:

```bash
streamlit run app.py
```

## ⚠️ Limitations

Real-world performance may vary depending on camera movement,
lighting, occlusion, and object size.

Near-duplicate video frames across dataset splits have not
been fully ruled out. Shot-counting statistics are not included.

## 👩‍💻 Developer

**Mai Mohammed**

Artificial Intelligence & Computer Vision

---

This is an independent educational project and is not
affiliated with the NBA or any basketball team.

Use and distribution must comply with the applicable
model, dataset, and media licensing terms.
