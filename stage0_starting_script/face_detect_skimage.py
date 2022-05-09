
import PIL.Image
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade
import matplotlib.pyplot as plt
from matplotlib import patches
import imageio
import sys
from os.path import join

# Load the trained file from the module root.
trained_file = data.lbp_frontal_face_cascade_filename()

# Initialize the detector cascade.
detector = Cascade(trained_file)

if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = join("../sample_images", "IMG-0311_xmas_2020.JPG")
    # image_path = join("sample_images", "owls.jpg")

img = imageio.imread(image_path)

detected = detector.detect_multi_scale(img=img,
                                       scale_factor=1.2,
                                       step_ratio=1,
                                       min_size=(60, 60),
                                       max_size=(600, 600))

plt.imshow(img)
img_desc = plt.gca()
plt.set_cmap('gray')

for patch in detected:

    img_desc.add_patch(
        patches.Rectangle(
            (patch['c'], patch['r']),
            patch['width'],
            patch['height'],
            fill=False,
            color='r',
            linewidth=2
        )
    )

img = PIL.Image.open(image_path)

data = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
data["Number of faces detected"] = len(detected)

print(data)

plt.show()
