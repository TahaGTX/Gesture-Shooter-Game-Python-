# 🎮 Gesture Shooter – Hand Tracking Game (Python)

Gesture Shooter is a **gesture-controlled arcade-style game** inspired by Fruit Ninja, built entirely using **Python**, **OpenCV**, and **MediaPipe**.

You aim using your **index finger** and shoot objects using a **pinch / fire gesture** detected via your webcam. The game features increasing difficulty, combo multipliers, lives, and a clean cyber-style UI.

---

## ✨ Features

* 🖐️ Real-time **hand tracking** using webcam
* 🔥 **Fire gesture detection** (index finger + thumb pinch)
* 🎯 **Combo multiplier** for fast consecutive hits
* ❤️ **Lives system** with Game Over screen
* 🧠 **AI difficulty scaling** (speed & spawn rate increase)
* 🕶️ Dark cyber-style UI
* 📷 Live **camera preview panel** (bottom-right)
* ⚡ Smooth gameplay (30–60 FPS depending on system)

---


## 🐍 Python Version (IMPORTANT)

✅ **Python 3.10.x is REQUIRED**

MediaPipe is sensitive to Python versions.
This project is tested and stable on **Python 3.10**.

Check your version:

```bash
python --version
```

---

## 🔧 Installation & Setup (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/TahaGTX/gesture-shooter-game-Python-.git
cd gesture-shooter-game
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell)**

```bash
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```bash
.venv\Scripts\activate
```

You should see:

```
(.venv)
```

---

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Run the Game 🎮

```bash
python game.py
```

Press **ESC** to exit.

---

## 🕹️ How to Play

* ☝️ **Index finger** → Aim
* 🤏 **Pinch (index + thumb)** → Shoot
* 🎯 Fast hits → Increase combo multiplier
* ❤️ Missed objects → Lose lives
* ☠️ 0 lives → Game Over

---

## 🧠 Difficulty Scaling

As your **score increases**:

* Objects move faster
* More objects spawn simultaneously
* Game becomes progressively harder

---

## 🧪 Common Issues & Fixes

### ❌ `AttributeError: module 'mediapipe' has no attribute 'solutions'`

Fix:

```bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.9
```

Also ensure:

* There is **NO file named `mediapipe.py`** in your project folder.

---

### ❌ Webcam Not Opening

* Close Zoom / Teams / Camera apps
* Ensure correct camera index in `game.py`:

```python
cv2.VideoCapture(0)
```

Try `1` if `0` doesn’t work.

---

## 📦 requirements.txt

Create a file named `requirements.txt` with this content:

```
opencv-python
numpy
mediapipe==0.10.9
```

---

## 🚀 Future Improvements

* 🔁 Restart game using gesture
* 🖥️ Fullscreen mode
* ⚡ Power-ups (slow motion, nuke, shield)
* 👹 Boss enemies
* 📊 High score saving
* 📦 Windows EXE build

---

## 📜 License

This project is open-source and free to use for **learning, experimentation, and personal projects**.

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 🧠 Improve it
