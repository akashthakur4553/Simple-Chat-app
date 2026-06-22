# Simple Chat App

![Deploy Status](https://img.shields.io/badge/deployed%20on-Render-blue)

A lightweight real‑time chat application built with **FastAPI**, **WebSockets**, and vanilla JavaScript.  The app demonstrates a minimal but production‑ready WebSocket setup, handling connections, broadcasting messages, and cleanly disconnecting clients when the browser tab closes.

---

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Demo

You can try the live version here: <https://simple-chat-app-zonl.onrender.com/>

---

## Features

- Real‑time bi‑directional communication using **WebSockets**
- Automatic user presence tracking (online/offline)
- Clean disconnection handling when a client closes the browser/tab
- Simple UI with message alignment (sender on right, others on left)
- No external front‑end framework – pure HTML, CSS, and JavaScript

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | **FastAPI** (Python 3.11) |
| WebSocket Server | `websockets` & Starlette internals |
| Front‑end | Vanilla HTML / CSS / JavaScript |
| Deployment | Render (Free tier) |
| Dependency Management | `requirements.txt` |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/akashthakur4553/Simple-Chat-app.git
cd Simple-Chat-app

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # macOS / Linux
# or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Running Locally

```bash
uvicorn app:app --reload
```

Open your browser and navigate to `http://127.0.0.1:8000/`. The chat UI will load and connect to `ws://127.0.0.1:8000/ws`.

---

## Deployment

The app is already deployed on Render.  The repository contains a `render.yaml` (if you want to customize) and the following environment variables are **not** required for the basic version.

To deploy your own copy:
1. Push the code to a GitHub repository.
2. Create a new **Web Service** on Render.
3. Set the **Build Command** to `pip install -r requirements.txt`.
4. Set the **Start Command** to `uvicorn app:app --host 0.0.0.0 --port $PORT`.
5. Render will automatically provision a URL similar to `https://<your‑app>.onrender.com/`.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome‑feature`).
3. Commit your changes and push to your fork.
4. Open a Pull Request against the `main` branch.


