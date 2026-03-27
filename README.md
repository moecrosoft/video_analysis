# 🎥 Video Analysis AI

An end-to-end AI application that analyzes uploaded videos, extracts frame-level understanding using vision models, and generates a natural language summary using large language models. This project combines computer vision (OpenCV + BLIP), a FastAPI backend, a Streamlit frontend, a PostgreSQL database, and full Dockerized deployment running on an AWS EC2 instance.

---

## 📌 Overview

Users can:
- Upload MP4 videos from the browser
- Get AI-generated descriptions of video scenes
- Receive a structured summary of what happens in the video
- View analysis history stored in the database

---

## 🧠 How It Works

1. **Upload** — User uploads a video via Streamlit UI
2. **Send** — Frontend sends video file to backend via `POST /analyse`
3. **Frame Extraction** — Backend reads video using OpenCV and samples frames
4. **Captioning** — Each sampled frame is processed using BLIP (Salesforce) to generate captions
5. **Summarization** — Captions are sent to LLaMA 3 (via Ollama) to generate a final summary
6. **Store** — Summary is saved in PostgreSQL
7. **Display** — Summary is returned and displayed in the UI
8. **History** — Past analyses are retrieved via `GET /history`

---

## 🏗️ Tech Stack

| Layer      | Technology                                              |
|------------|---------------------------------------------------------|
| Backend    | FastAPI, OpenCV, PyTorch, Hugging Face Transformers, psycopg2 |
| AI Models  | BLIP (Salesforce), LLaMA 3 (Ollama)                    |
| Frontend   | Streamlit                                               |
| Database   | PostgreSQL                                              |
| DevOps     | Docker, Docker Compose, AWS EC2                         |

---

## 📂 Project Structure
```
video_scene_analyzer/
│
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── db.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started
```bash
git clone https://github.com/your-username/video_scene_analyzer.git
cd video_scene_analyzer
docker-compose up -d --build
```

This starts:
- **Frontend** → http://localhost:8501
- **Backend** → http://localhost:8000
- **PostgreSQL** database → running in container

---

## 🔗 API Reference

### `POST /analyse`

**Request:**
```json
{
  "file": "video.mp4"
}
```

**Response:**
```json
{
  "summary": "A man is walking down a street while cars pass by...",
  "frames_analysed": 12
}
```

### `GET /history`

**Response:**
```json
[
  {
    "filename": "video.mp4",
    "summary": "A person is walking outside...",
    "created_at": "2026-03-27 15:00:00"
  }
]
```

---

## 🤖 Model Details

| Component      | Value                                        |
|----------------|----------------------------------------------|
| Vision Model   | Salesforce BLIP                              |
| LLM            | LLaMA 3 (via Ollama)                         |
| Input          | Video frames extracted using OpenCV          |
| Output         | Natural language summary                     |
| Framework      | PyTorch + Transformers                       |
| Strategy       | Frame sampling + caption aggregation         |

---

## 🎯 Features

- ✅ Video upload and AI analysis
- ✅ Frame-by-frame caption generation
- ✅ LLM-based summarization
- ✅ PostgreSQL history tracking
- ✅ Fully Dockerized system running on AWS EC2
- ✅ Clean Streamlit UI
- ✅ End-to-end vision + language pipeline
