import cv2
import os
import csv
import numpy as np

def average_hash(image, hash_size=8):
    img = cv2.imread(image)
    img = cv2.resize(img, [hash_size, hash_size])
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    pixels = img_gray.flatten()
    avg = pixels.mean()
    diff = pixels > avg
    diff = diff * 1
    # print(diff)
    rdiff = 0
    for d in diff:
        if d == 1:
            rdiff+=1
    ratio = rdiff / 64.0
    hash_value = np.packbits(diff)
    return hash_value, ratio

def main(inputPath):
    images = os.listdir(inputPath)
    file = open('/media/data2/cropland/0_samples/cropland.csv', 'w')
    writer = csv.writer(file)
    for image in images:
        hash_value, ratio = average_hash(inputPath + image)
        # print(ratio)
        writer.writerow([image.split('/')[-1], ratio, hash_value])
    # writer.close()
    file.close()

if __name__ == '__main__':
    main('/media/data2/cropland/0_samples/img/')