import cv2
import sys
from matplotlib.pyplot import imshow, show


def collect_detected_faces(image_path, casc_path=None, draw_rectangles=False,
                           show_image=False):
    if casc_path is None:
        casc_path = "haarcascade_frontalface_default.xml"

    # Create the haar cascade
    face_cascade = cv2.CascadeClassifier(casc_path)

    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.imread(image_path, 0)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        # flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    if draw_rectangles:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2, 4)

    if show_image:
        imshow(image)
        show()

    return faces, image


if __name__ == "__main__":
    # Get user supplied values
    imagePath = sys.argv[1]
    cascPath = "haarcascade_frontalface_default.xml"

    faces, image = collect_detected_faces(imagePath, draw_rectangles=True,
                                          show_image=True)
    print("Found {0} faces!".format(len(faces)))
