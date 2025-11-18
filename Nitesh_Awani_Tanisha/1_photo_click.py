import cv2

# Open webcam (0 is the default camera)
cap = cv2.VideoCapture(0)# can click photos or videos
#cap is an object made from cv2
cap.set(cv2.CAP_PROP_FPS, 15)#providing the cap object an custom fps
#but the camera driver is not accepting the request and therefore we have to wokr defauls fps = 30.0;
while True:
    ret, frame = cap.read()
    #ret true if camera is working fine, otherwise false
    #frame is actual picture captured by camera in a matrix form (RGB)  
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    if not ret:# if camera is not connected
        print("Failed to grab frame")
        break

    cv2.imshow("Camera", frame)# show clicked picture or live camera

    # Press 'c' to capture photo
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite("captured_photo.jpg", frame)
        print("Photo captured and saved as captured_photo.jpg")
        break

# Release and close windows
cap.release()
cv2.destroyAllWindows()
