import cv2


# 图片清晰度识别
def getImageVar(imgPath):
    image = cv2.imread(imgPath);
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar


print(getImageVar('abc.jpg'))
