#full working code # (press escape to toggle the "project on-off")
import threading
# shared flag between threads
click_flag = threading.Event()  
double_click_flag = threading.Event()  
scroll_and_go_down_flag = threading.Event()
scroll_and_go_up_flag = threading.Event()
keyboard_flag = threading.Event()
#notes 
#frame == image
#double-click == right click
#click = left click

#buttons functionality, runs as separate thread
def run_overlay():

    def open_virtual_keyboard():#running as a separate thread
        import os
        os.system("osk")

    import tkinter as tk
    import pyautogui

    RADIUS = 30
    COLOR = "lime"
    BORDER = 3
    UPDATE_INTERVAL = 10  # ms
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "black")
    root.overrideredirect(True)

    screen_width, screen_height = pyautogui.size()
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black', highlightthickness=0)
    canvas.pack()

    circle = canvas.create_oval(0, 0, 0, 0, outline=COLOR, width=BORDER)

    def update_circle():
        x, y = pyautogui.position()
        canvas.coords(circle, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
        root.after(UPDATE_INTERVAL, update_circle)


    #  Four Clickable Circles on Screen Edges 
    edge_radius = 60
    edge_color = "#78bafc"   # border color
    edge_fill = "#7cb7f3"    # light blue fill
    edge_border = 2

    # Default colors
    edge_colors = {
        "active": "#5cf05c",   # bright green when ON
        "inactive": "#7cb7f3"  # light blue when OFF
    }
    # Circle center coordinates
    edge_positions = {
        "top":    (screen_width / 2, edge_radius + 10),
        "bottom": (screen_width / 2, screen_height - edge_radius - 10),
        "left":   (edge_radius + 10, screen_height / 2),
        "right":  (screen_width - edge_radius - 10, screen_height / 2),
        "keyboard":  (0.1*screen_width, screen_height - edge_radius - 10)
    }
    edge_circles = {}

    # Function to handle circle clicks
    def on_circle_click(event, name):
        global click_flag
        print(f"{name} circle clicked!")
        if name=="right":
            if click_flag.is_set():
                click_flag.clear()
                print("click_flag OFF")
                # Change circle color to inactive
                canvas.itemconfig(edge_circles["right"], fill=edge_colors["inactive"])
            else:
                click_flag.set()
                double_click_flag.clear();                canvas.itemconfig(edge_circles["left"], fill=edge_colors["inactive"])
                scroll_and_go_down_flag.clear();          canvas.itemconfig(edge_circles["bottom"], fill=edge_colors["inactive"])
                scroll_and_go_up_flag.clear();            canvas.itemconfig(edge_circles["top"], fill=edge_colors["inactive"])
                keyboard_flag.clear();                    canvas.itemconfig(edge_circles["keyboard"], fill=edge_colors["inactive"])
                print("click_flag ON")
                canvas.itemconfig(edge_circles["right"], fill=edge_colors["active"])
        if name=="left":
            if double_click_flag.is_set():
                double_click_flag.clear()
                print("double_click_flag OFF")
                # Change circle color to inactive
                canvas.itemconfig(edge_circles["left"], fill=edge_colors["inactive"])
            else:
                double_click_flag.set()
                click_flag.clear();                       canvas.itemconfig(edge_circles["right"], fill=edge_colors["inactive"])
                scroll_and_go_down_flag.clear();          canvas.itemconfig(edge_circles["bottom"], fill=edge_colors["inactive"])
                scroll_and_go_up_flag.clear();            canvas.itemconfig(edge_circles["top"], fill=edge_colors["inactive"])
                keyboard_flag.clear();                    canvas.itemconfig(edge_circles["keyboard"], fill=edge_colors["inactive"])
                print("double_click_flag ON")
                canvas.itemconfig(edge_circles["left"], fill=edge_colors["active"])
        if name =="bottom":
            if scroll_and_go_down_flag.is_set():
                scroll_and_go_down_flag.clear()
                print("scroll_and_go_down_flag OFF")
                # Change circle color to inactive
                canvas.itemconfig(edge_circles["bottom"], fill=edge_colors["inactive"])
            else:
                scroll_and_go_down_flag.set()
                click_flag.clear();                       canvas.itemconfig(edge_circles["right"], fill=edge_colors["inactive"])
                double_click_flag.clear();                canvas.itemconfig(edge_circles["left"], fill=edge_colors["inactive"])
                scroll_and_go_up_flag.clear();            canvas.itemconfig(edge_circles["top"], fill=edge_colors["inactive"])
                keyboard_flag.clear();                    canvas.itemconfig(edge_circles["keyboard"], fill=edge_colors["inactive"])
                print("scroll_and_go_down_flag ON")
                canvas.itemconfig(edge_circles["bottom"], fill=edge_colors["active"])
        if name =="top":
            if scroll_and_go_up_flag.is_set():
                scroll_and_go_up_flag.clear()
                print("scroll_and_go_up_flag OFF")
                # Change circle color to inactive
                canvas.itemconfig(edge_circles["top"], fill=edge_colors["inactive"])
            else:
                scroll_and_go_up_flag.set()
                click_flag.clear();                       canvas.itemconfig(edge_circles["right"], fill=edge_colors["inactive"])
                double_click_flag.clear();                canvas.itemconfig(edge_circles["left"], fill=edge_colors["inactive"])
                scroll_and_go_down_flag.clear();          canvas.itemconfig(edge_circles["bottom"], fill=edge_colors["inactive"])
                keyboard_flag.clear();                    canvas.itemconfig(edge_circles["keyboard"], fill=edge_colors["inactive"])
                print("scroll_and_go_up_flag ON")
                canvas.itemconfig(edge_circles["top"], fill=edge_colors["active"])
        if name =="keyboard":
            if keyboard_flag.is_set():
                keyboard_flag.clear()
                print("keyboard_flag OFF")
                # Change circle color to inactive
                canvas.itemconfig(edge_circles["keyboard"], fill=edge_colors["inactive"])
            else:
                keyboard_flag.set()
                click_flag.clear();                       canvas.itemconfig(edge_circles["right"], fill=edge_colors["inactive"])
                double_click_flag.clear();                canvas.itemconfig(edge_circles["left"], fill=edge_colors["inactive"])
                scroll_and_go_down_flag.clear();          canvas.itemconfig(edge_circles["bottom"], fill=edge_colors["inactive"])
                scroll_and_go_up_flag.clear();            canvas.itemconfig(edge_circles["top"], fill=edge_colors["inactive"])
                print("keyboard_flag ON")

                # os.system("osk")#open virtual keypad
                thread = threading.Thread(target=open_virtual_keyboard,daemon=True)
                thread.start()
                
                canvas.itemconfig(edge_circles["keyboard"], fill=edge_colors["active"])

    # Create 4 circles with clickable bindings
    edge_labels = {}

    for name, (cx, cy) in edge_positions.items():
        circle_edge = canvas.create_oval(
            cx - edge_radius, cy - edge_radius,
            cx + edge_radius, cy + edge_radius,
            fill=edge_colors["inactive"], outline=edge_color, width=edge_border,
            tags=name
        )
        edge_circles[name] = circle_edge  # store reference
        # Add text label on each circle
        label_text = {
            "top": "Scroll-Down",
            "bottom": "Scroll-Up",
            "left": "Right-Click",
            "right": "Left-Click",
            "keyboard":"KeyBoard"
        }[name]

        text_item = canvas.create_text(
            cx, cy, text=label_text,
            fill="white", font=("Arial", 11, "bold")
        )
        edge_labels[name] = text_item
        # Bind left-click to each circle
        canvas.tag_bind(name, "<Button-1>", lambda e, n=name: on_circle_click(e, n))
        canvas.tag_bind(text_item, "<Button-1>", lambda e, n=name: on_circle_click(e, n))


    update_circle()
    root.mainloop()




def run_camera():

    #captures images at approx 30 fps
    #convert raw images to gray color (for used by dlib)
    #detect faces in images
    #detects 68 landmarks in images
    #detects eyes only landmarks
    #detects centers and stores prev_landarks of eye
    #Cursor movement is capable 
    #Clicks on-off is possible
    #all 5 clicks possible

    import cv2
    import dlib
    import numpy as np
    import time
    import pyautogui
    pyautogui.FAILSAFE = False#check boundry meet
    #setups 
    PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat" # Provides landmarks
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    detector = dlib.get_frontal_face_detector()

    cap = cv2.VideoCapture(0)# 0 is indicating to use default camera
    #cap is an object of cv2 library and VideoCapture captures actaull an image again and again  
    project_flag=False#activate deadctivate this clicks and cursor movement
    prev_left_eye_landmarks =[]
    prev_right_eye_landmarks =[]
    prev_mouse_position = []#stores prev 10 mouse position coordinates
    prev_mouse_position_len_threshold = 10#stores prev 10 mouse position coordinates
    flag = 0#used to know whether prev_land_mark exist
    x_direction_multiplication_factor = 40#multiplies the chnage in x_cordinates of eye landmarks to a constant to obtain x_cordinates change of for device
    y_direction_multiplication_factor = 20
    movement_detection_threshold = 0.6
    #helps in click decision..
    screen_width, screen_height = pyautogui.size()
    edge_radius = 60
    right_center= [screen_width - edge_radius - 10, screen_height / 2]
    left_center= [edge_radius + 10, screen_height / 2]
    bottom_center =  [screen_width / 2, screen_height - edge_radius - 10]
    top_center = [screen_width / 2, edge_radius + 10]
    keyboard_center =   [0.1*screen_width, screen_height - edge_radius - 10]


    def center_avg_of_eye_landmarks(lst):
        x_lst = [ele[0] for ele in lst]
        y_lst = [ele[1] for ele in lst]

        x_center = int(sum(x_lst)/len(x_lst))
        y_center = int(sum(y_lst)/len(y_lst))
        center = (x_center,y_center)
        return center

    def move_ment(prev_left_eye_center,left_eye_center,prev_right_eye_center,right_eye_center):#return the avg_change in eyes position 
        x_change_left = left_eye_center[0]-prev_left_eye_center[0]
        x_change_right = right_eye_center[0]-prev_right_eye_center[0]
        x_change_avg = (x_change_left+x_change_right)/2

        y_change_left = left_eye_center[1]-prev_left_eye_center[1]
        y_change_right = right_eye_center[1]-prev_right_eye_center[1]
        y_change_avg = (y_change_left+y_change_right)/2
        return [x_change_avg,y_change_avg]
    
    def clicks(prev_mouse_position,radius,expected_number_of_position_within_circle,center=None):#use to detect a click on screen
        if center is None:#center are provided for checking for center on edges(left-click,right-click,scroll,keyboard)
            x_list = [ele[0] for ele in prev_mouse_position]
            y_list = [ele[1] for ele in prev_mouse_position]

            x_center_avg = int(sum(x_list)/len(x_list))
            y_center_avg = int(sum(y_list)/len(y_list))

            center = [x_center_avg,y_center_avg]

        count =0
        for ele in prev_mouse_position:
            if(abs(center[0]-ele[0])<=radius and abs(center[1]-ele[1])<=radius):
                count +=1
        
        if(count>=expected_number_of_position_within_circle):
            return [True,center]
        else:
            return [False,center]
    
    def prev_mouse_pos_update(prev_mouse_position,position):#just removes oldest position and add new position in the prev_mouse_position array
        lst = prev_mouse_position[1:]
        lst.append(position)
        return lst
    

    #MAIN LOOP.......................................
    try:
        prev_time = time.time()#will be used in calculating actual FPS
        while True:
            #frame ======= img 
            ret, frame = cap.read()
            if not ret:#if camera is not connected (ret is an boolean return from opencv refreing to camera is connected or not)
                break
            fps=cap.get(cv2.CAP_PROP_FPS)#getting fps from camera driver, deafult and not-changeable for this hardware is 30.0
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converting the raw image to gray color so that dlib can perform better on the image

            faces = detector(gray_frame)#dlib detects faces from the image (just face area)
            for face in faces:
                x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
                cv2.rectangle(gray_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)#make square boundary on gray image
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)#make squre boundary on raw image

                landmarks = predictor(gray_frame, face)#find landmarks in gray frame (or gray image)
                # print(landmarks)#python binded object and cant print
                #(we can use all 68 landmarks for movement detection but for now we will just use eye landmarks only, as we are focusing on eye tracking only)
                left_eye_landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in [36, 37, 38, 39, 40, 41]]
                right_eye_landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in [42, 43, 44, 45, 46, 47]]

                # Draw landmarks
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
                
                if flag:#flag ==1 (Comparing & Movement)

                    # print("prev_left_eye_landmarks",prev_left_eye_landmarks,"center",center_avg_of_eye_landmarks(prev_left_eye_landmarks))
                    cv2.circle(gray_frame, center_avg_of_eye_landmarks(prev_left_eye_landmarks), 2, (0,0,255), -1)
                    cv2.circle(frame, center_avg_of_eye_landmarks(prev_left_eye_landmarks), 2, (0,0,255), -1)
                    print('')
                    # print("prev_right_eye_landmarks",prev_right_eye_landmarks,"center",center_avg_of_eye_landmarks(prev_right_eye_landmarks))
                    cv2.circle(gray_frame, center_avg_of_eye_landmarks(prev_right_eye_landmarks), 2, (0,0,255), -1)
                    cv2.circle(frame, center_avg_of_eye_landmarks(prev_right_eye_landmarks), 2, (0,0,255), -1)
                    print('')
                    # print("left_eye_landmarks", left_eye_landmarks,"center",center_avg_of_eye_landmarks(left_eye_landmarks))
                    cv2.circle(gray_frame, center_avg_of_eye_landmarks(left_eye_landmarks), 2, (0,255,0), -1)
                    cv2.circle(frame, center_avg_of_eye_landmarks(left_eye_landmarks), 2, (0,255,0), -1)
                    print('')
                    # print("right_eye_landmarks", right_eye_landmarks,'center',center_avg_of_eye_landmarks(right_eye_landmarks))
                    cv2.circle(gray_frame, center_avg_of_eye_landmarks(right_eye_landmarks), 2, (0,255,0), -1)
                    cv2.circle(frame, center_avg_of_eye_landmarks(right_eye_landmarks), 2, (0,255,0), -1)

                    avg_movement = move_ment(center_avg_of_eye_landmarks(prev_left_eye_landmarks),center_avg_of_eye_landmarks(left_eye_landmarks),center_avg_of_eye_landmarks(prev_right_eye_landmarks),center_avg_of_eye_landmarks(right_eye_landmarks))
                    print("avg_movement ", avg_movement)

                    if project_flag==False:continue#does not move cursor in this case

                    if(abs(avg_movement[0])>movement_detection_threshold or abs(avg_movement[1])>movement_detection_threshold):
                        pyautogui.moveRel(-x_direction_multiplication_factor*avg_movement[0],y_direction_multiplication_factor*avg_movement[1],0.1)#move cursor from one position to another (relative and not positioned)
                    
                    prev_left_eye_landmarks=left_eye_landmarks
                    prev_right_eye_landmarks=right_eye_landmarks
            #above for loop ends here
            #CLICK decision
            if(project_flag==True):
                x,y = pyautogui.position()#get mouse's current position coordinates
                position = [x,y]
                if(len(prev_mouse_position)<prev_mouse_position_len_threshold):
                    prev_mouse_position.append(position)
                else:
                    #decide click
                    decision = clicks(prev_mouse_position,30,5)#detects a click 
                    if(decision[0]==True):
                        x_click_center = decision[1][0]
                        y_click_center = decision[1][1]

                        decision_right = clicks(prev_mouse_position,60,5,right_center)
                        decision_left = clicks(prev_mouse_position,60,5,left_center)
                        decision_bottom = clicks(prev_mouse_position,60,5,bottom_center)
                        decision_top = clicks(prev_mouse_position,60,5,top_center)
                        decision_keyboard = clicks(prev_mouse_position,60,5,keyboard_center)

                        if decision_right[0] ==True:#left click
                            #click is on right center
                            pyautogui.click(right_center[0],right_center[1])  #after clicking, the tkinter will catch click and turn off clicking
                            prev_mouse_position=[]
                        elif decision_left[0]==True:#right click  
                            #click is on left center
                            pyautogui.click(left_center[0],left_center[1])  #after clicking, the tkinter will catch click and turn off double-clicking
                            prev_mouse_position=[]
                        elif decision_bottom[0]==True:#scroll down
                            pyautogui.click(bottom_center[0],bottom_center[1])  #after clicking, the tkinter will catch click and turn off scrolling
                            prev_mouse_position=[]
                        elif decision_top[0]==True:#scroll top
                            pyautogui.click(top_center[0],top_center[1])  #after clicking, the tkinter will catch click and turn off scrolling
                            prev_mouse_position=[]
                        elif decision_keyboard[0]==True:
                            pyautogui.click(keyboard_center[0],keyboard_center[1])  #after clicking, the tkinter will catch click and turn off keyboard
                            prev_mouse_position=[]
                        else:
                            #click is at normal place on screen and not on any of the 5 circles
                            if(double_click_flag.is_set() and click_flag.is_set()):
                                pyautogui.doubleClick(x_click_center,y_click_center)#over-power of double click
                                prev_mouse_position=[]
                            elif(double_click_flag.is_set()):
                                pyautogui.doubleClick(x_click_center,y_click_center)#over-power of double click
                                prev_mouse_position=[]
                            elif(click_flag.is_set()):
                                pyautogui.click(x_click_center,y_click_center)#simple left click
                                prev_mouse_position=[]
                            elif(scroll_and_go_down_flag.is_set()):
                                pyautogui.scroll(-100)
                                prev_mouse_position=[]
                            elif(scroll_and_go_up_flag.is_set()):
                                pyautogui.scroll(100)
                                prev_mouse_position=[]
                            #does not click anywhere
                    #remove last most and add newest position
                    prev_mouse_position=prev_mouse_pos_update(prev_mouse_position,position)

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

            if cv2.waitKey(1) & 0xFF == 27:#Press escape to exit from clicks and movement
                if (project_flag):
                    project_flag = False
                else:
                    project_flag = True
    finally:
        cap.release()#delete that cv2 object
        cv2.destroyAllWindows()#destroy cv2 window

# ==== MULTI-THREADING ====
# Run overlay and camera in parallel threads
overlay_thread = threading.Thread(target=run_overlay, daemon=True)
overlay_thread.start()

run_camera()
