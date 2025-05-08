# EyeOnFocus
![ChatGPT Image May 8, 2025, 12_32_53 AM](https://github.com/user-attachments/assets/bb762b3f-4b14-4bfe-b328-22e2986e22d1) - AI-Powered Focus Assistant
EyeOnFocus is an intelligent desktop application built using Python, MediaPipe, and OpenCV to help improve focus during study or work sessions. The tool uses computer vision to monitor eye and mouth movements, detecting when you are not focused (e.g., by yawning, closing your eyes for too long, or looking away from the screen). It provides real-time feedback with animated icons and alerts, encouraging you to stay on task.

Key Features:
Eye Movement Monitoring: Detects when you keep your eyes closed for too long, with a customizable threshold.

Yawning Detection: Alerts when yawning is detected, indicating potential tiredness or loss of focus.

Look-Away Detection: Identifies when you look away from the screen for a set duration.

Real-time Focus Timer: Tracks the time you spend in focus mode and displays it on the UI.

Alert System: Plays a sound alert and changes on-screen status icons when focus is broken.

Interactive UI: Provides visual feedback using animated icons and labels to show focus status.

Log Events: Tracks events such as "Eyes Closed Too Long", "Yawning Detected", and "Looking Away Too Long" in a log file for review.

Requirements:
Python 3.x

mediapipe

opencv-python

playsound

tkinter

threading

Installation:
Clone the repository:
git clone https://github.com/ComputerVision804/EyeOnFocus.git
Install the required libraries:

pip install -r requirements.txt
Run the application:

python main.py
How It Works:
The app uses your webcam to monitor your facial features in real-time. It detects eye movements, yawns, and head turns using facial landmark tracking provided by MediaPipe. If any of these events are detected (eyes closed too long, yawning, or looking away), the app alerts you with a sound and visual icon. It also tracks how long you've been focused and displays the time on the UI.
![img](https://github.com/user-attachments/assets/d17316a9-fbff-4186-a9e1-1e193ed4f63c)

Future Improvements:
Enhanced AI for emotion recognition.
Integration with productivity apps for automatic session tracking.
