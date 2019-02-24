import PIL.Image
from PIL.ExifTags import TAGS
import sys

from face_detect import collect_detected_faces

if __name__ == "__main__":

    image_path = sys.argv[1]
    img = PIL.Image.open(image_path)

    data = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
    faces, _ = collect_detected_faces(image_path=image_path)
    data["Number faces"] = len(faces)
    print(data)
