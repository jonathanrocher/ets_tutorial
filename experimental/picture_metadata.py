import PIL.Image
from PIL.ExifTags import TAGS
import sys

from face_detect import collect_detected_faces


def collect_metadata(image_path):
    """ Use PIL to extract EXIF information from jpeg image files.
    """
    img = PIL.Image.open(image_path)

    data = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
    faces, _ = collect_detected_faces(image_path=image_path)
    data["Number faces"] = len(faces)
    return data


if __name__ == "__main__":

    image_path = sys.argv[1]
    data = collect_metadata(image_path)
    print(data)
