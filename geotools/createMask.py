import cv2
import os
import difflib

import numpy as np

def createBlackMask(imagePath, outputPath):
    fileName = imagePath.split("/")[-1]
    fileList = os.listdir(imagePath)
    bounddir = difflib.get_close_matches("boundary", fileList)
    for bound in bounddir:
        images = os.listdir(os.path.join(imagePath, bound, 'image/'))
        # labels = os.listdir(os.path.join(imagePath, bound, 'label/labelme/'))
        images.sort()
        # labels.sort()
        imagesarr = []
        # labelsarr = []
        for image in images:
            imagesarr.append((image.split('/')[-1]).split('.')[0])
        # for label in labels:
        #     labelsarr.append((label.split('/')[-1]).split('_')[0])

        # output = list(set(imagesarr).symmetric_difference(set(labelsarr))) # 差集
        # print(bound + ' 文件中未包含mask的图片数量为: ' + str(len(output)))
        for out in imagesarr:
            image = cv2.imread(imagePath)
            mask = np.zeros([1024, 1024])
            cv2.imwrite(outputPath + out + "_mask.tif", mask)
            # outputPath + fileName + '-' + (bound[0]).upper() + bound[-1] + '-' + 

def testMaskandIamgeSum(imagePath, maskPath):
    # imagePath = os.path.join(imagePath, 'boundary1/image/')
    images = list(os.listdir(imagePath))
    masks = list(os.listdir(maskPath))
    print(len(images) == len(masks))

if __name__ == '__main__':
    testMaskandIamgeSum("/media/data2/cropland/0_samples/img/", "/media/data2/cropland/0_samples/label/")