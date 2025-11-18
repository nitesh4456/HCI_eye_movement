import cv2
import dlib
import numpy as np
import time
import math

import pyautogui
pyautogui.FAILSAFE = False #stops pyautogui to check 

PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
EYE_AR_THRESH = 0.23         # Threshold for blink detection
EYE_AR_CONSEC_FRAMES = 3     # Consecutive frames to confirm a blink

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

def get_eye_points(landmarks, eye_indices):
    """Return eye landmark points as list of (x, y)."""
    return [(landmarks.part(i).x, landmarks.part(i).y) for i in eye_indices]

def eye_aspect_ratio(eye):
    """Compute Eye Aspect Ratio (EAR)."""
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

def get_change_in_center_of_eye(lst1,lst2):##-->left_eye:  [(344, 300), (354, 294), (365, 292), (377, 297), (366, 301), (355, 303)]
    #lst1 older postion , lst2 newer position
    lst1_x=[ele[0] for ele in lst1]
    c1_x= round(sum(lst1_x)/len(lst1_x))

    lst1_y=[ele[1] for ele in lst1]
    c1_y= round(sum(lst1_y)/len(lst1_y))

    lst2_x=[ele[0] for ele in lst2]
    c2_x= round(sum(lst2_x)/len(lst2_x))

    lst2_y=[ele[1] for ele in lst2]
    c2_y= round(sum(lst2_y)/len(lst2_y))

    # eye_position_change_distance = round(math.sqrt((abs(c1_x-c2_x)^2)+(abs(c1_y-c2_y)^2)))
    result =[]
    result.append(c2_x-c1_x)#chnage in x direction 
    result.append(c2_y-c1_y)#change in y direction 

    return result

import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

blink_counter, total_blinks = 0, 0
prev_time = time.time()

# Target FPS
target_fps = 20
frame_time = 1.0 / target_fps

left_eye_prev = [(344, 300), (354, 294), (365, 292), (377, 297), (366, 301), (355, 303)]
right_eye_prev = [(344, 300), (354, 294), (365, 292), (377, 297), (366, 301), (355, 303)]

try:
    while True:
        start_time = time.time()  # mark loop start

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
            
            left_eye_movement_distance = get_change_in_center_of_eye(left_eye_prev, left_eye)
            right_eye_movement_distance = get_change_in_center_of_eye(right_eye_prev, right_eye)

            avg_change_x_distance = (left_eye_movement_distance[0] + right_eye_movement_distance[0])/2
            avg_change_y_distance = (left_eye_movement_distance[1] + right_eye_movement_distance[1])/2

            # avg_eye_movement_distance = round((left_eye_movement_distance + right_eye_movement_distance) / 2)
            print("Change Distance in x is :", avg_change_x_distance)
            print("Change Distance in y is :", avg_change_y_distance)

            change_x = 40*avg_change_x_distance
            change_y = 20*avg_change_y_distance

            if(abs(avg_change_x_distance)>0.6 or abs(avg_change_y_distance)>0.6):
                pyautogui.moveRel(-change_x,change_y,0.1)

            left_eye_prev = left_eye
            right_eye_prev = right_eye

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
                    print("Blink1")
                    #pyautogui.click(x=100, y=200) # Clicks the left mouse button at coordinates (100, 200)
                    # pyautogui.click()
                    # pyautogui.doubleClick()
                blink_counter = 0

            # Display EAR and blink count
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f"Blinks: {total_blinks}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # --- FPS calculation & display ---
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {fps:.1f}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Eye Movement Detection", frame)

        # --- Enforce fixed FPS ---
        elapsed = time.time() - start_time
        wait_time = max(0, frame_time - elapsed)
        time.sleep(wait_time)

        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()


print('''
1.Capable of eye movement tracker
2.Capable of tracking blinks
3.Capable of moving cursor
''')