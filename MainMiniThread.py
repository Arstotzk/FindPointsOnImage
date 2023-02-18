from PIL import Image
import configRead
import ImageOperations

if __name__ == '__main__':
    image = Image.open("img/1prepare2.jpg")
    imageOper = ImageOperations.ImageOperations(image, configRead.Settings())
    imageOper.findPointsByTemplate()
    print("Executing time: " + str(imageOper.executionTime()))
    imageOper.setPointsOnImege()
    imageOper.image.show()
