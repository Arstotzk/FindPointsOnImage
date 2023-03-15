from PIL import Image
import config_read
from normalization import Normalization
from image_operations import ImageOperations

if __name__ == '__main__':
    image = Image.open("img/2prepare.jpg")
    norm = Normalization(image)
    norm.normalize()
    imageOper = ImageOperations(norm.imgNormalize, config_read.Settings())
    imageOper.find_points_by_template()
    imageOper.find_cephalometric_params()
    imageOper.print_cephalometric_params()
    print("Executing time: " + str(imageOper.execution_time()))
    imageOper.set_points_on_image()
    imageOper.image.show()
