#captures images at approx 30 fps
#convert raw images to gray color (for used by dlib)
#detect faces in images
#detects 68 landmarks in images
#detects eyes only landmarks
#detects centers and stores prev_landarks of eye
#Cursor movement is capable 

import cv2
import dlib
import numpy as np
import time
import pyautogui
pyautogui.FAILSAFE = False
#setups 
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat" # Provides landmarks
predictor = dlib.shape_predictor(PREDICTOR_PATH)
detector = dlib.get_frontal_face_detector()

cap = cv2.VideoCapture(0)# 0 is indicating to use default camera
#cap is an object of cv2 library and VideoCapture captures actaull an image again and again  

prev_left_eye_landmarks =[]
prev_right_eye_landmarks =[]
flag = 0

def center_avg_of_eye_landmarks(lst):
    x_lst = [ele[0] for ele in lst]
    y_lst = [ele[1] for ele in lst]

    x_center = int(sum(x_lst)/len(x_lst))
    y_center = int(sum(y_lst)/len(y_lst))
    center = (x_center,y_center)
    return center

                # pyautogui.moveRel(-change_x,change_y,0.1)

def move_ment(prev_left_eye_center,left_eye_center,prev_right_eye_center,right_eye_center):
    x_change_left = left_eye_center[0]-prev_left_eye_center[0]
    x_change_right = right_eye_center[0]-prev_right_eye_center[0]
    x_change_avg = (x_change_left+x_change_right)/2

    y_change_left = left_eye_center[1]-prev_left_eye_center[1]
    y_change_right = right_eye_center[1]-prev_right_eye_center[1]
    y_change_avg = (y_change_left+y_change_right)/2

    return [x_change_avg,y_change_avg]


try:
    prev_time = time.time()#will be used in calculating actual FPS
    while True:
        #frame ======= img 
        ret, frame = cap.read()
        if not ret:#if camera is not connected
            break

        fps=cap.get(cv2.CAP_PROP_FPS)#getting fps from camera driver.
        # print("FPS: ",fps)#deafult and not-changeable for this hardware is 30.0

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converting the raw image to gray color so that dlib can perform better on the image

##############################################################
        faces = detector(gray_frame)
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(gray_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)#make square boundary on gray image
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)#make squre boundary on raw image

            landmarks = predictor(gray_frame, face)#find landmarks in gray frame (or gray image)
            # print(landmarks)#python binded object and cant print
            #(we can use all 68 landmarks for movement detection but for now we will just use eye landmarks only, as we are focusing on eye tracking only)
            left_eye_landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in [36, 37, 38, 39, 40, 41]]
            right_eye_landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in [42, 43, 44, 45, 46, 47]]

            # Draw contours
            for ele in left_eye_landmarks:
                    x= ele[0]
                    y=ele[1]
                    cv2.circle(gray_frame, (x, y), 2, (255, 0, 0), -1)
                    cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
            for ele in right_eye_landmarks:
                x= ele[0]
                y=ele[1]
                cv2.circle(gray_frame, (x, y), 2, (255, 0, 0), -1)
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

            if not flag : #flag ==0 
                prev_left_eye_landmarks = left_eye_landmarks
                prev_right_eye_landmarks = right_eye_landmarks
                flag = 1
            
            if flag:#flag ==1 (comparing and movement)









                print("prev_left_eye_landmarks",prev_left_eye_landmarks,"center",center_avg_of_eye_landmarks(prev_left_eye_landmarks))
                cv2.circle(gray_frame, center_avg_of_eye_landmarks(prev_left_eye_landmarks), 2, (0,0,255), -1)
                cv2.circle(frame, center_avg_of_eye_landmarks(prev_left_eye_landmarks), 2, (0,0,255), -1)
                print('')
                print("prev_right_eye_landmarks",prev_right_eye_landmarks,"center",center_avg_of_eye_landmarks(prev_right_eye_landmarks))
                cv2.circle(gray_frame, center_avg_of_eye_landmarks(prev_right_eye_landmarks), 2, (0,0,255), -1)
                cv2.circle(frame, center_avg_of_eye_landmarks(prev_right_eye_landmarks), 2, (0,0,255), -1)
                print('')
                print("left_eye_landmarks", left_eye_landmarks,"center",center_avg_of_eye_landmarks(left_eye_landmarks))
                cv2.circle(gray_frame, center_avg_of_eye_landmarks(left_eye_landmarks), 2, (0,255,0), -1)
                cv2.circle(frame, center_avg_of_eye_landmarks(left_eye_landmarks), 2, (0,255,0), -1)
                print('')
                print("right_eye_landmarks", right_eye_landmarks,'center',center_avg_of_eye_landmarks(right_eye_landmarks))
                cv2.circle(gray_frame, center_avg_of_eye_landmarks(right_eye_landmarks), 2, (0,255,0), -1)
                cv2.circle(frame, center_avg_of_eye_landmarks(right_eye_landmarks), 2, (0,255,0), -1)

                avg_movement = move_ment(center_avg_of_eye_landmarks(prev_left_eye_landmarks),center_avg_of_eye_landmarks(left_eye_landmarks),center_avg_of_eye_landmarks(prev_right_eye_landmarks),center_avg_of_eye_landmarks(right_eye_landmarks))
                print("avg_movement ", avg_movement)

                if(abs(avg_movement[0])>0.6 or abs(avg_movement[1])>0.6):
                    pyautogui.moveRel(-40*avg_movement[0],20*avg_movement[1],0.1)

                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                
                prev_left_eye_landmarks=left_eye_landmarks
                prev_right_eye_landmarks=right_eye_landmarks
            
            



###########################################################EXTRA PART#####################################
        # --- Actual FPS calculation & display ---
        curr_time = time.time()
        actual_fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        #Time text writing on frame (images)
        cv2.putText(frame, f"Actual FPS: {actual_fps:.1f}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Deafult FPS: {fps:.1f}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(gray_frame, f"Actual FPS: {actual_fps:.1f}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(gray_frame, f"Deafult FPS: {fps:.1f}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Camera:'30' Pictures per second in BGR color",frame)# shows frames images again and agian which looks like live video but it is image
        cv2.imshow("Gray:'30' Pictures per second in Gray color",gray_frame)

        if cv2.waitKey(1) & 0xFF == 27:#Press escape to exit
            break
finally:
    cap.release()#delete that cv2 object
    cv2.destroyAllWindows()#destroy cv2 window
