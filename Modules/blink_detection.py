import cv2
import dlib
import numpy as np
import time

# ========================
# CONFIGURATION
# ========================
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
EYE_AR_THRESH = 0.23         # Threshold for blink detection
EYE_AR_CONSEC_FRAMES = 3     # Consecutive frames to confirm a blink

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

# ========================
# HELPER FUNCTIONS
# ========================
def get_eye_points(landmarks, eye_indices):
    """Return eye landmark points as list of (x, y)."""
    return [(landmarks.part(i).x, landmarks.part(i).y) for i in eye_indices]

def eye_aspect_ratio(eye):
    """Compute Eye Aspect Ratio (EAR)."""
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

# ========================
# MAIN LOOP
# ========================
cap = cv2.VideoCapture(0)
blink_counter, total_blinks = 0, 0
prev_time = time.time()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            # Extract eyes
            left_eye = get_eye_points(landmarks, [36, 37, 38, 39, 40, 41])
            right_eye = get_eye_points(landmarks, [42, 43, 44, 45, 46, 47])

            # Draw contours
            cv2.polylines(frame, [np.array(left_eye, np.int32)], True, (0, 255, 0), 1)
            cv2.polylines(frame, [np.array(right_eye, np.int32)], True, (0, 255, 0), 1)

            # EAR
            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

            # Blink detection
            if ear < EYE_AR_THRESH:
                blink_counter += 1
            else:
                if blink_counter >= EYE_AR_CONSEC_FRAMES:
                    total_blinks += 1
                blink_counter = 0

            # Display EAR and blink count
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f"Blinks: {total_blinks}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Show FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {fps:.1f}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Eye Movement Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

finally:
    cap.release()
    cv2.destroyAllWindows()

print('''
1.Capable of eye movement tracker
2.Capable of tracking blinks
''')