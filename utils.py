import math

def euclidean_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def eye_aspect_ratio(landmarks, eye_indices):
    A = euclidean_dist(landmarks[eye_indices[1]], landmarks[eye_indices[5]])
    B = euclidean_dist(landmarks[eye_indices[2]], landmarks[eye_indices[4]])
    C = euclidean_dist(landmarks[eye_indices[0]], landmarks[eye_indices[3]])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(landmarks):
    # Use actual landmark indexes from the full 468-point MediaPipe mesh
    top_lip = landmarks[13]      # upper lip center
    bottom_lip = landmarks[14]   # lower lip center
    left_corner = landmarks[78]
    right_corner = landmarks[308]

    vertical = euclidean_dist(top_lip, bottom_lip)
    horizontal = euclidean_dist(left_corner, right_corner)
    mar = vertical / horizontal
    return mar
