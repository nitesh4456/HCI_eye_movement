import dlib
import cv2

detector = dlib.get_frontal_face_detector()
img = cv2.imread("u42.jpg")
cv2.imshow("img1",img)

# Convert to grayscale (works better)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = detector(gray)

print("Number of faces detected:", len(faces))

# Draw rectangles around faces
for face in faces:
    x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Detected Faces", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
