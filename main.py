import cv2
import time
import tkinter as tk
from itertools import cycle
from datetime import datetime
import threading
import mediapipe as mp
import numpy as np

# ==================== Face & Landmark Setup ====================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

LEFT_EYE = [33, 160, 158, 133]
RIGHT_EYE = [362, 385, 387, 263]
MOUTH = [13, 14, 78, 308]

LOOK_AWAY_THRESH = 0.35
EYE_AR_THRESH = 0.2
YAWN_THRESH = 20
CLOSE_EYE_TIME = 2.0
LOOK_AWAY_TIME = 3.0

# ==================== Logging ====================
log_file = open("focus_log.txt", "a")

def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{timestamp}] {event}\n")
    log_file.flush()

# ==================== Utility Functions ====================
def eye_aspect_ratio(landmarks, eye_indices):
    left = np.array(landmarks[eye_indices[0]])
    right = np.array(landmarks[eye_indices[3]])
    top = np.array(landmarks[eye_indices[1]])
    bottom = np.array(landmarks[eye_indices[2]])
    hor_dist = np.linalg.norm(left - right)
    ver_dist = np.linalg.norm(top - bottom)
    return ver_dist / hor_dist if hor_dist != 0 else 0

def mouth_aspect_ratio(landmarks, mouth_indices):
    top = np.array(landmarks[mouth_indices[0]])
    bottom = np.array(landmarks[mouth_indices[1]])
    left = np.array(landmarks[mouth_indices[2]])
    right = np.array(landmarks[mouth_indices[3]])
    ver = np.linalg.norm(top - bottom)
    hor = np.linalg.norm(left - right)
    return (ver / hor) * 100 if hor != 0 else 0

# ==================== GUI Setup ====================
root = tk.Tk()
root.title("🧠 Study Buddy AI")
root.geometry("400x250")
root.configure(bg="#1e1e2f")

focus_label = tk.Label(root, text="Focus Status", font=("Helvetica", 18), fg="white", bg="#1e1e2f")
focus_label.pack(pady=10)

emoji_cycle = cycle(["🔆", "📚", "🧠", "✅", "⏳"])
icon_label = tk.Label(root, text="", font=("Helvetica", 40), bg="#1e1e2f")
icon_label.pack(pady=10)

progress = tk.DoubleVar()
progress_bar = tk.Scale(root, variable=progress, from_=0, to=100, orient="horizontal", length=300,
                        label="Focus Progress", fg="white", bg="#1e1e2f", troughcolor="#4CAF50", font=("Helvetica", 10))
progress_bar.pack(pady=10)

# ==================== Timer for Focus Session ====================
start_time = time.time()

def update_focus_progress():
    elapsed = time.time() - start_time
    progress.set(min(100, (elapsed / 1800) * 100))  # 30-minute session
    root.after(1000, update_focus_progress)

def update_icon():
    icon_label.config(text=next(emoji_cycle))
    root.after(1000, update_icon)

# ==================== Camera & Detection Thread ====================
def detection_loop():
    cap = cv2.VideoCapture(0)
    close_eye_start, look_away_start = None, None

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if result.multi_face_landmarks:
            for face in result.multi_face_landmarks:
                landmarks = [(lm.x * w, lm.y * h) for lm in face.landmark]

                left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
                right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
                mar = mouth_aspect_ratio(landmarks, MOUTH)

                ear = (left_ear + right_ear) / 2.0

                # Check if eyes closed
                if ear < EYE_AR_THRESH:
                    if close_eye_start is None:
                        close_eye_start = time.time()
                    elif time.time() - close_eye_start > CLOSE_EYE_TIME:
                        focus_label.config(text="⚠️ Eyes Closed Too Long")
                        log_event("Eyes Closed Too Long")
                else:
                    close_eye_start = None

                # Check yawn
                if mar > YAWN_THRESH:
                    focus_label.config(text="😮 Yawn Detected")
                    log_event("Yawn Detected")

                # Look away detection
                nose = landmarks[1]
                if nose[0] < w * LOOK_AWAY_THRESH or nose[0] > w * (1 - LOOK_AWAY_THRESH):
                    if look_away_start is None:
                        look_away_start = time.time()
                    elif time.time() - look_away_start > LOOK_AWAY_TIME:
                        focus_label.config(text="👀 Looking Away Too Long")
                        log_event("Looking Away Too Long")
                else:
                    look_away_start = None

        cv2.imshow('Study Buddy Feed', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    log_file.close()

# ==================== Run App ====================
threading.Thread(target=detection_loop, daemon=True).start()
update_focus_progress()
update_icon()
root.mainloop()
